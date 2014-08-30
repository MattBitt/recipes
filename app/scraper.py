import urllib2
#import requests
from BeautifulSoup import BeautifulSoup as BS


class RecipeScraper:
    def __init__(self, url):
        self.url = url
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent', 'Google Chrome')]
        self.soup = BS(self.opener.open(self.url))
        
class AllRecipes(RecipeScraper):
    def get_title(self):
        return self.soup.find('h1', {'id':'itemTitle'}).text
  
    def get_ingredients(self):
        ingredient_list = []
        ingredient_names = self.soup.findAll('span', {'class' : 'ingredient-name'})
        for nm in ingredient_names:
            ingredient_amount = nm.findPrevious('span')
            ingredient_list.append( ingredient_amount.text + ' ' + nm.text )
        return "\n".join(item for item in ingredient_list)
    
    def get_directions(self):
        directions = self.soup.findAll('div', {'itemprop' : 'recipeInstructions'})
        directions_list = []
        for row in directions:
            d = row.findAll('li')
            for di in d:
                directions_list.append(di.text)
        return "\n".join(item for item in directions_list)

class SkinnyTaste(RecipeScraper):
    def get_title(self):
        return self.soup.find('h3', {'class':'post-title entry-title'}).text
  
    def get_ingredients(self):
        ingreds = self.soup.findAll('div', {'class':'post-body entry-content'})
        ingredient_list = []
        for row in ingreds:
            d = row.findAll('li')
            for di in d:
                ingredient_list.append(di.text)
        return "\n".join(item for item in ingredient_list)
        
    
    def get_directions(self):
        directions = self.soup.findAll('div', {'class':'post-body entry-content'})
        directions_list = []
        started = False
        for content in directions[0].contents:
            try:
                
                if len(content.strip()) > 10 and started == True:
                    directions_list.append( content.strip() )
                if content.strip() == "Directions:":
                    started = True
            except:
                pass
        return "\n".join(item for item in directions_list)
        

def scrape_recipe( url ):
    if url.lower().find('allrecipes.com') > -1:
        return AllRecipes( url )
    elif url.lower().find('skinnytaste.com') >-1:
        return SkinnyTaste( url )
    else:
        return None
        

        
        
if __name__ == '__main__':
        r = SkinnyTaste("http://www.skinnytaste.com/2014/08/asian-farro-medley-with-salmon.html")
        #import pdb; pdb.set_trace()
        print r
        print r.get_title()
        print r.get_ingredients()
        print r.get_directions()