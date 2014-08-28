from lxml import html
import requests

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
        ingred_list = []
        counter = 1
        while True:
            ingred_xpath = '//*[@id="Blog1"]/div[1]/div/div/div/div[1]/div[2]/ul[1]/li[' + str(counter) + ']/text()'
            if self.tree.xpath(ingred_xpath) != []:
                ingred_list.append(self.tree.xpath(ingred_xpath))
                counter += 1
            else:
                break
        
        return ingred_list
        
    def get_directions(self):
        directions = []
        counter = 1
        while counter == 1 or direc != []:
            direc_xpath = '//*[@id="Blog1"]/div[1]/div/div/div/div[1]/div[2]/text()[' + str(counter) + ']'
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
    
#ar = AllRecipes("http://allrecipes.com/Recipe/Chef-Johns-Salt-Roasted-Chicken/Detail.aspx?soid=recs_recipe_5")
#print ar.get_title()
#print ar.get_ingredients()
#print ar.get_directions()

#t = SkinnyTasteRecipe('http://www.skinnytaste.com/2014/08/grilled-veggie-towers-with-mozzarella.html#more')
#print st.get_title()
#print st.get_ingredients()
#rint st.get_directions()
def scrape_recipe( recipe_url ):
    recipe = SkinnyTaste(url=recipe_url)
    return recipe
    #print recipe.get_ingredients()
    #print recipe.get_directions()




