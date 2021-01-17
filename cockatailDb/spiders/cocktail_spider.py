import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from string import ascii_lowercase

class CocktailSpiderSpider(CrawlSpider):
    name = 'cocktail_spider'
    allowed_domains = ['thecocktaildb.com']
    #start_urls = ['http://thecocktaildb.com/']

    rules = (Rule(LinkExtractor(allow=r"drink/[0-9]+$"), callback="parse_drink", follow=False),)
    def start_requests(self):
        start_urls = ['https://thecocktaildb.com/browse.php?b=%s' % c for c in ascii_lowercase]
        #start_urls=['https://thecocktaildb.com/browse.php?b=a']
        for url in start_urls:
            yield scrapy.Request(url)

    def parse_drink(self, response):
        trans_table = {ord(c): None for c in u'\r\n\t'}

        #parse the name. Can't seem to parse anything
        name =''.join(t.strip().translate(trans_table) for t in response.xpath("/html/body/section/div[1]/div/table/tr[1]/td[1]/h2//text()").extract())
        #/html/body/section/div[1]/div/table/tbody/tr[1]/td[1]/h2
        #parse the ingrediens
        ingredients_list = []
        for ingredients in response.xpath('//figcaption/text()'):
        	ingredients_list.append(ingredients.extract().replace("  ", " "))
        #Parsing the note
        note = response.xpath('/html/body/section/div[1]/div/table/tr[2]/td[1]/div/a/text()').extract()

        #parsed instructions and glass
        text = ' '.join(s.strip().translate(trans_table) for s in response.xpath("/html/body/section/div[1]/div/text()").extract())
        splitText = [x.strip() for x in text.split('.')]
        glass = splitText.pop().replace("Serve:",'').strip()
        print(splitText)
        yield {
        	'name': name,
            'label': note,
            'variant': [{
                'origin': "thecocktailDb",
                'url' : response.url,
        		'ingredients': ingredients_list,
        		'instructions': splitText,
            	'Glass': glass
            }]
        }

