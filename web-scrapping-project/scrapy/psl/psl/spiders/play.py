import scrapy


class PlaySpider(scrapy.Spider):
    name = "play"
    allowed_domains = ["www.espncricinfo.com"]
    start_urls = [
        "https://www.espncricinfo.com/series/pakistan-super-league-2023-24-1412744/match-schedule-fixtures-and-results"
    ]

    def parse(self, response):
        links = response.css(
            "div.ds-grow.ds-px-4.ds-border-r.ds-border-line-default-translucent"
        )

        for link in links:
            href = link.css("a::attr(href)").get()
            if "/full-scorecard" in href:
                url = "https://www.espncricinfo.com" + href.replace(
                    "/full-scorecard", "/ball-by-ball-commentary"
                )
                yield response.follow(url, callback=self.parse_data)

    def parse_data(self, response):
        cards = response.css(
            "div.ds-text-tight-m.ds-font-regular.ds-flex.ds-px-3.ds-py-2"
        )
        for card in cards:
            elements = card.css("div span::text").getall()
            ball = elements[0]
            result = elements[1]
            players = elements[2]
            print("ball:", ball)
            print("result:", result)
            print("players:", players)
