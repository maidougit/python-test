import scrapy


# µÁ”∞ÃÏÃ√
class DyttSpider(scrapy.Spider):
    name = "dytt"
    start_urls = [
        'https://www.dytt8.net/',
    ]

    def parse(self, response):
        movies = response.css('div.co_content8')[0].css('td.inddline[height="22"]')[1:]
        for movie in movies:
            movie_href = movie.css("a::attr(href)")[1].get()
            yield response.follow(movie_href,callback = self.movieparse)

    def movieparse(self,response):
        yield {
            'movie_name':response.css("div.title_all font::text").get(),
            'download_link':response.css('table td[bgcolor="#fdfddf"] a::text').get()
        }