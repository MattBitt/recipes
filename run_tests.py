import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../'))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/mytests')
import unittest
 
# Import your test classes
from tests.form_test import FormTest


# For the Code Coverage Report
from coverage import coverage
cov = coverage(branch = True, omit = ['env/*', 'run_tests.py', 'tests/*'])
cov.start()
 
 
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FormTest))
    #suite.addTest(unittest.makeSuite(MyAppUnitTest))
    #suite.addTest(unittest.makeSuite(MainSiteTest))
    #suite.addTest(unittest.makeSuite(ManagerSiteTest))
    
    return suite
    
 
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    import pdb
    pdb.set_trace()
    try:
        runner.run(test_suite)
 
    except:
        pass
    
    cov.stop()
 
    print "\n\nCoverage Report:\n"
    cov.report()
    
    cov.erase()