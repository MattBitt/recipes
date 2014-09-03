import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../'))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\\mytests')
import unittest

from datetime import datetime, timedelta, date
from app.models import Recipe
from config import basedir
from app import app, db
from app.scraper import scrape_recipe
from flask import url_for, session
from app.forms import RecipeForm
from pyquery import PyQuery as pq
 
# Import your test classes
from form_tests import FormTests
from db_tests import DB_Tests
from scraper_tests import ScraperTests



# For the Code Coverage Report
# from coverage import coverage
# cov = coverage(branch = True, omit = ['src/*', 'run_tests.py', 'mytests/*', 'db_*'])
# cov.start()
 
 
def suite(add_slow = False):
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FormTests))
    suite.addTest(unittest.makeSuite(DB_Tests))
    if add_slow:
        suite.addTest(unittest.makeSuite(ScraperTests))
    return suite
    
 
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'a':
            test_suite = suite(True)
    else:
        print "Not all tests are being run.  Please append 'a' to the command to run every test"
        test_suite = suite(False)
    try:
        app.logger.info('Starting Test Suite')
        runner.run(test_suite)
        app.logger.info('Finished Testing')
 
    except:
        pass
    
#cov.stop()
 
   # print "\n\nCoverage Report:\n"
    #cov.report()
    
    #cov.erase()