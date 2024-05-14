import scrapy
from urllib.parse import urlencode

API_KEY = '9cb39971-d2fe-40f6-88ee-231f375f4a7d'

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class CompaniesSpider(scrapy.Spider):
    """This spider wil crawl all the company link available in itviec and save it
    to a json line file.
    """
    name = "companies"
    start_urls = [
        'https://itviec.com/companies',
    ]

    HEADERS = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"proxy": "http://proxy_address:port"},
            )

    def parse(self, response):
        all_companies = response.xpath("//div[@class='first-group companies']/a[@class='featured-company']/@href").getall()

        for company_link in all_companies:
            relative_link = '/'.join(company_link.split('/')[:-1])
            company_name = company_link.split('/')[-2]
            absolute_link = response.urljoin(relative_link)
            print("======")
            print(company_name)
            print("======")
            yield {'company_name': company_name, 'url': absolute_link}

        next_page = response.xpath("//a[@class='more-jobs-link more-company']/@href").get()
        # next_page now has the form of '/companies?page=2' or None

        if next_page is not None:
            # makes absolute url
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

