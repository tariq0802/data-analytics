import scrapy
from cdata.spiders.keywords import KEYWORDS
from cdata.items import CdataItem
from datetime import datetime
from cdata.pipelines import CdataPipeline


class CricketSpider(scrapy.Spider):
    name = "cricket"
    allowed_domains = ["www.espncricinfo.com"]
    start_urls = ["https://www.espncricinfo.com/ci/engine/series/index.html"]

    def __init__(self, *args, **kwargs):
        super(CricketSpider, self).__init__(*args, **kwargs)
        self.pipeline = CdataPipeline()

    def parse(self, response):
        archive = response.xpath(
            '//*[@id="viewport"]/div[7]/div[2]/main/section/section[4]'
        )
        links = archive.css(
            "section.season-block section.season-links a::attr(href)"
        ).getall()[2:20]
        for link in links:
            url = "https://www.espncricinfo.com/" + link
            yield response.follow(url, callback=self.parse_season)

    def parse_season(self, response):
        t20i = response.xpath(
            '//*[@id="viewport"]/div[7]/div[2]/main/section/section[7]'
        )
        t20l = response.xpath(
            '//*[@id="viewport"]/div[7]/div[2]/main/section/section[10]'
        )
        for element in [t20i, t20l]:
            series = element.css("div.teams")
            for match_element in series:
                link = match_element.css("a::attr(href)").get()
                title = match_element.css("a::text").get()
                if (
                    any(keyword.lower() in title.lower() for keyword in KEYWORDS)
                    and "qualifier" not in title.lower()
                    and "region" not in title.lower()
                ):
                    yield response.follow(link, callback=self.parse_series)

    def parse_series(self, response):
        matches = response.css("div.ds-grow.ds-px-4.ds-border-r")
        for match in matches:
            link = match.css("a::attr(href)").get()
            url = "https://www.espncricinfo.com/" + link

            if not self.pipeline.link_exists_in_database(url):
                self.pipeline.save_link_to_database(url)
                yield response.follow(url, callback=self.parse_match)

    def parse_match(self, response):
        info = response.css("div.ds-grow div.ds-text-tight-m::text").get()
        series = response.css("div.ds-grow div.ds-text-tight-m span::text").get()
        date, place, match_no = self.parse_info(info)
        teams = response.css("div.ds-items-center.ds-min-w-0 a span::text").getall()

        try:
            for i in range(1, 3):
                xpath = (
                    f"//div[@class='ds-rounded-lg ds-mt-2'][{i}]/div/div[2]/table[1]"
                )
                batting = response.xpath(xpath)
                batters = batting.css("td.ds-w-0.ds-min-w-max.ds-flex")
                runs = batting.css("td.ds-w-0.ds-min-w-max strong::text").getall()
                balls = batting.css("td:nth-child(4)::text").getall()
                fours = batting.css("td:nth-child(6)::text").getall()
                sixes = batting.css("td:nth-child(7)::text").getall()
                strike = batting.css("td:nth-child(8)::text").getall()

                for index, batter in enumerate(batters):
                    name = batter.css("a span::text").get()
                    item = CdataItem(
                        date=date,
                        series=series,
                        venue=place,
                        match_no=match_no,
                        team=teams[0] if i == 1 else teams[1],
                        name=name,
                        run=runs[index],
                        ball=balls[index],
                        four=fours[index],
                        six=sixes[index],
                        sr=strike[index],
                    )
                    yield item
        except Exception as e:
            pass

        try:
            for i in range(1, 3):
                xpath = (
                    f"//div[@class='ds-rounded-lg ds-mt-2'][{i}]/div/div[2]/table[2]"
                )
                bowling = response.xpath(xpath)
                bowlers = bowling.css("td.ds-flex.ds-items-center")
                overs = bowling.css("td:nth-child(2)::text").getall()
                maidens = bowling.css("td:nth-child(3)::text").getall()
                runs_given = bowling.css("td:nth-child(4)::text").getall()
                wickets = bowling.css("td:nth-child(5) strong::text").getall()
                economy = bowling.css("td:nth-child(6)::text").getall()
                wides = bowling.css("td:nth-child(10)::text").getall()
                no_balls = bowling.css("td:nth-child(11)::text").getall()

                for index, element in enumerate(bowlers):
                    bowler = element.css("a span::text").get()
                    item = CdataItem(
                        date=date,
                        series=series,
                        venue=place,
                        match_no=match_no,
                        bowling_team=teams[1] if i == 1 else teams[0],
                        bowler=bowler,
                        over=overs[index],
                        maiden=maidens[index],
                        given=runs_given[index],
                        wicket=wickets[index],
                        eco=economy[index],
                        wide=wides[index],
                        nb=no_balls[index],
                    )
                    yield item
        except Exception as e:
            pass

    def parse_info(self, info):
        info_parts = info.split(", ")
        date_parts = info_parts[-2:]
        date_str = " ".join(date_parts)
        try:
            parsed_date = datetime.strptime(date_str, "%B %d %Y")
            place = info_parts[-3:-2][0].split(" (")[0]
            match_no = info_parts[0].split(" ")[0]
        except Exception as e:
            parts = date_str.split(" ")
            day = parts[1] if "-" in date_str else parts[1]
            date_str_fixed = " ".join([parts[0], day, date_parts[-1]])
            parsed_date = datetime.strptime(date_str_fixed, "%B %d %Y")
            place = "-"
            match_no = "-"
        date = parsed_date.strftime("%Y-%m-%d")

        return date, place, match_no
