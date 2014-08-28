from lxml import html
import requests
import BeautifulSoup as BS
import re
class RecipeScraper:
    def __init__( self, url ):
        self.page = requests.get(self.url)
        self.tree = html.fromstring(self.page.text)

    def get_title(self):
        self.title = self.tree.xpath(self.title_xpath)
        return self.title[0]
        
    
class AllRecipes (RecipeScraper):
    def __init__(self, url):
        self.url = url
        self.title_xpath = '//*[@id="itemTitle"]/text()'
        RecipeScraper.__init__(self, url)
    
    def get_ingredients(self):
        ingred_names = self.tree.xpath('//*[@id="lblIngName"]/text()')
        ingred_amounts = self.tree.xpath('//*[@id="lblIngAmount"]/text()')
        ingreds = zip(ingred_amounts, ingred_names)

        ingred_list = []
        for ingred in ingreds:
            ingred_list.append(' '.join(ingred))
    
        ingred_list = '\n'.join(ingred_list)
        return ingred_list
        
    def get_directions(self):
        directions = []
        counter = 1
        while counter == 1 or direc != []:
            first = False
            direc = self.tree.xpath('//*[@id="zoneRecipe"]/div[1]/div[11]/div/ol/li[' + str(counter) + ']/span/text()')
            directions.append(direc)
            counter += 1

        directions.pop()
        direcs = ""

        for d in directions:
            direcs += d[0] + '\n'
        return direcs
    
class SkinnyTaste (RecipeScraper):
    def __init__(self, url):
        self.url = url
        self.title_xpath = '//*[@id="Blog1"]/div[1]/div/div/div/div[1]/div[2]/b/text()'
        RecipeScraper.__init__(self, url)

    def get_ingredients(self):
        ingred_xpath = '//*[@id="Blog1"]/div[1]/div/div/div/div[1]/div[2]/ul[1]/li[1]/text()'
        counter = 1
        ingred_string = ""
        while True:
            ingred_xpath = '//*[@id="Blog1"]/div[1]/div/div/div/div[1]/div[2]/ul[1]/li[' + str(counter) + ']/text()'
            if self.tree.xpath(ingred_xpath) != []:
                ingred_string += str(self.tree.xpath(ingred_xpath)[0]) + '\n'
                counter += 1
            else:
                return ingred_string[:-1]
        
    def get_directions(self):
        directions = []
        
        bs = BS.BeautifulSoup("<html><a>sometext</a></html>")
        print bs.find('a').string
        
        
        exit()
        counter = 1
        while counter == 1 or direc != []:
            direc_xpath = '//*[@id="Blog1"]/div[1]/div/div/div/div[1]/div[2]/text()'
            direc = self.tree.xpath(direc_xpath)
            if direc != []:
                print direc
                directions.append(direc)
                counter += 1
            else:
                break

        #directions.pop()
        direcs = ""
        for d in directions:
            direcs += d[0] + '\n'
        return direcs

        
class ZipList(RecipeScraper):
    def __init__(self, url):
        self.url = url
        print self.url
        
        self.title_xpath = '//*[@id="title"]/div[2]/h1/text()'
        self.ingred_xpath = '//*[@id="left"]/div[1]/ul'
        RecipeScraper.__init__(self, url)
        
    def get_ingredients( self ):
        print self.tree.xpath(self.ingred_xpath) 
        
                
                
                
    def get_title(self):
        print self.tree.xpath(self.title_xpath)


#ar = AllRecipes("http://allrecipes.com/Recipe/Chef-Johns-Salt-Roasted-Chicken/Detail.aspx?soid=recs_recipe_5")
#print ar.get_title()
#print ar.get_ingredients()
#print ar.get_directions()

#t = SkinnyTasteRecipe('http://www.skinnytaste.com/2014/08/grilled-veggie-towers-with-mozzarella.html#more')
#print st.get_title()
#print st.get_ingredients()
#rint st.get_directions()
def scrape_recipe( recipe_url ):
    recipe = ZipList(url=recipe_url)
    return recipe
    #print recipe.get_ingredients()
    #print recipe.get_directions()

if __name__ == '__main__':
    #r = scrape_recipe('http://www.skinnytaste.com/2014/08/grilled-veggie-towers-with-mozzarella.html')
    r =ZipList(url='http://www.ziplist.com/recipes/soft-cheese-bread/45a80b00-662e-0130-8069-123138123252')
    print r.get_title()
    print r.get_ingredients()
    #print r.get_directions()

