import os
import unittest
from datetime import datetime, timedelta, date
from app.models import User, Recipe
from config import basedir
from app import app, db
from app.scraper import scrape_recipe
from flask import url_for
from tests   import BaseCase


class SlowTests(BaseCase):
    def test_scrape_all_recipes(self):
        url = "http://allrecipes.com/Recipe/Grilled-Salmon-I/Detail.aspx?soid=carousel_0_rotd&prop24=rotd"
        rec = scrape_recipe( url )
        assert rec.get_title() == "Grilled Salmon I"
        assert "lemon pepper to taste" in rec.get_ingredients()
        assert "vegetable oil until" in rec.get_directions()
  
    def test_scrape_skinny_taste(self):
        url = 'http://www.skinnytaste.com/2014/08/asian-farro-medley-with-salmon.html'
        rec = scrape_recipe( url )
        assert rec.get_title() == "Asian Farro Medley with Salmon"
        assert "1 tbsp oyster sauce" in rec.get_ingredients()
        assert "salmon to marinade and set" in rec.get_directions()

if __name__ == '__main__':
    unittest.main()