import scrapy


class CdataItem(scrapy.Item):
    date = scrapy.Field()
    series = scrapy.Field()
    venue = scrapy.Field()
    match_no = scrapy.Field()
    team = scrapy.Field()
    name = scrapy.Field()
    run = scrapy.Field()
    ball = scrapy.Field()
    four = scrapy.Field()
    six = scrapy.Field()
    sr = scrapy.Field()

    bowling_team = scrapy.Field()
    bowler = scrapy.Field()
    over = scrapy.Field()
    maiden = scrapy.Field()
    given = scrapy.Field()
    wicket = scrapy.Field()
    eco = scrapy.Field()
    wide = scrapy.Field()
    nb = scrapy.Field()

    play_no = scrapy.Field()
    player = scrapy.Field()
