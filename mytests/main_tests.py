if __name__ == '__main__':
    import os, sys
    basedir = os.path.abspath(os.path.dirname(__file__) + '/../')
    sys.path.insert(0, basedir)
 
from app import app, db
from hakaru_test import MyAppTest
from pyquery import PyQuery as pq
 
from app.model import *

#http://www.axcella.com/~nicka/blog/?p=148
 
#
# Functional tests for Flask routes
class MainSiteTest(MyAppTest):
    
    # def test_hakaru_index(self):
        # rv = self.app.get('/')
        
        # # Make sure we got an OK response
        # self.assertEqual(rv.status_code, 200)
    
    # # Test the Singup Page
    # def test_signup(self):
        # rv = self.app.get('/signup')
        
        # # Make sure we got an OK response
        # self.assertEqual(rv.status_code, 200)
        
        # data = {}
        
        # # Posting empty data to signup for should generate alerts
        # rv = self.app.post('/signup', data=data)
        # self.assertEqual(rv.status_code, 200)
        # q = pq(rv.data)
        # alerttext = q('.alert').text()
        
        # assert 'First Name' in alerttext
        # assert 'Last Name' in alerttext
        # assert 'Organization Name' in alerttext
        # assert 'Invitation Code' in alerttext
        # assert 'E-Mail Address' in alerttext
        # assert 'Password' in alerttext
        # assert 'Accept TOS' in alerttext
        
        
        # # Now submitting with "real" data should not produce errors
        # #    and should result in new database entries
        # data = {
            # 'invite_code': 'AskMeAboutGofers',
            # 'email':       'testuser@test.com',
            # 'orgname':     'My Test Organization',
            # 'givenname':   'Test',
            # 'surname':     'User',
            # 'password':    'asdf1234',
            # 'confirm':     'asdf1234',
            # 'accept_tos':  'y'
        # }
        
        # rv = self.app.post('/signup', data=data)
        # self.assertEqual(rv.status_code, 302)       # On success we redirect
 
        # # Check that database entries were created
        # u = User.query.filter_by(email=data['email']).all()
        
        # self.assertEqual(len(u), 1, 'Incorrect number of users created')
        # self.assertEqual(u.givenname, data['givenname'])
        
        # o = Organization.query.filter_by(name='My Test Organization').all()
        
        # self.assertEqual(len(o), 1, 'Incorrect number of organizations created')
        
        # ou = OrganizationUsers.query.filter_by(organization_id=o[0].id, user_id=u[0].id, role='owner').all()
        
        # self.assertEqual(len(ou), 1, 'Incorrect number of organization user records created')
        
 
 
if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass