import scrapy
from cdata.items import CdataItem


class PlayingSpider(scrapy.Spider):
    name = "playing"
    allowed_domains = ["www.espncricinfo.com"]
    start_urls = [
        "https://www.espncricinfo.com/series/pakistan-super-league-2023-24-1412744/match-schedule-fixtures-and-results"
    ]

    def parse(self, response):
        link_elements = response.xpath("//div[@class='ds-p-0']/div")
        for element in link_elements:
            link = element.css("div div.ds-grow a::attr(href)").get()
            link_parts = link.split("/")
            link_joined = "/".join(link_parts[:-1])
            url = "https://www.espncricinfo.com" + link_joined + "/match-playing-xi"
            yield response.follow(url, callback=self.parse_player)

    def parse_player(self, response):
        try:
            name_elements = response.xpath("//tbody/tr")
            info = response.css("div.ds-font-regular.ds-text-typo-mid3::text").get()
            parts = info.split(", ")[0]
            match_no = parts.split(" ")[0]
            if name_elements:
                for name_element in name_elements[:11]:
                    names = name_element.css(
                        "div.ds-popper-wrapper.ds-inline a span::text"
                    ).getall()
                    for element in names:
                        name = element.replace("(c)", "").replace("†", "")
                        item = CdataItem(play_no=match_no, player=name.strip())
                        yield item
        except Exception as e:
            pass
