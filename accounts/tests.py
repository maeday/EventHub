"""
A collection of tests for the accounts app.

You can run these by running "./manage.py test accounts".
"""

from django.contrib.auth.models import User

from django.test import TestCase, LiveServerTestCase
from django.test.client import Client
from django.test.utils import override_settings

from accounts.forms import EmailUserCreationForm, EmailAuthenticationForm

class UserRegistrationFormTest(TestCase):
    """
    Tests to check that the EmailUserCreationForm works properly.
    """
    
    def test_email_invalid(self):
        """
        Tests that an invalid email address will not work.
        """
        params = {
            'email':'blah',
            'password1':'blah',
            'password2':'blah',
            'first_name':'blah',
            'last_name':'blah',
            'fbid': -1
        }
        form = EmailUserCreationForm(params)
        self.assertFalse(form.is_valid(), "Invalid email should not pass!")
        self.assertNotIn('password1', form._errors)
        self.assertNotIn('password2', form._errors)
        self.assertNotIn('first_name', form._errors)
        self.assertNotIn('last_name', form._errors)
        self.assertNotIn('fbid_name', form._errors)
        self.assertEqual(form._errors['email'][0], 
                         "Enter a valid e-mail address.")
        
    def test_passwords_different(self):
        """
        Tests that different passwords will not work.
        """
        params = {
            'email':'blah@blah.com',
            'password1':'blah1',
            'password2':'blah',
            'first_name':'blah',
            'last_name':'blah',
            'fbid': -1
        }
        form = EmailUserCreationForm(params)
        self.assertFalse(form.is_valid(), "Mis-matched passwords should not pass!")
        self.assertNotIn('email', form._errors)
        self.assertNotIn('password1', form._errors)
        self.assertNotIn('first_name', form._errors)
        self.assertNotIn('last_name', form._errors)
        self.assertNotIn('fbid_name', form._errors)
        self.assertEqual(form._errors['password2'][0], 
                         "The two password fields didn't match.")

class AccountViewsTest(TestCase):
    """
    Set of tests tha check to make sure the views are loading the correct 
    templates.
    """
    
    def test_registration_page_loads(self):
        c = Client()
        response = c.get('/register')
        
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
        # Check that correct templates are loaded
        self.assertTemplateUsed(response, 'header.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertTemplateUsed(response, 'accounts/register-1.html')
    
    def test_login_page_loads(self):
        c = Client()
        response = c.get('/login')
        
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
        # Check that correct templates are loaded
        self.assertTemplateUsed(response, 'header.html')
        self.assertTemplateUsed(response, 'footer.html')
        self.assertTemplateUsed(response, 'accounts/login.html')

@override_settings(
   EMAIL_HOST = 'localhost',
   EMAIL_PORT = 1025,
   EMAIL_HOST_USER = '',
   EMAIL_HOST_PASSWORD = ''
)
class UserRegistrationFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    ### Tests ###
    
    def test_register_user_2(self):
        """
        Tests that user is created from second user registration page
        """
        new_email = 'test@test.com'
        
        # Check to make sure user doesn't already exist
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email=new_email)
        
        # Register as new user
        fields = {
            'first_name' : 'Test',
            'last_name' : 'User',
            'email' : new_email,
            'password1' : 'test',
            'password2' : 'test',
            'fbid' : -1
        }
        response = self.client.post('/register', fields, follow=True)
        
        # Check that view redirects properly
        self.assertRedirects(response, "/login?register=success", 302, 200)
        
        # Checks to make sure user was created
        u = User.objects.get(email=new_email)
        self.assertIsNotNone(u)
        self.assertIsNotNone(u.get_profile())
        
    def test_login(self):
        """
        Test log in flow
        """
        user = self.create_user()
        fields = {
            'email' : 'test@test.com',
            'password' : 'test'
        }
        
        # Try to log in without activating user (should fail)
        response = self.client.post('/login', fields, follow=True)
        self.assertFormError(response, 'form', None, 
            ['This account is inactive. Please check your email for the ' +
             'activation link. If you have lost it, or it has expired, ' +
             'please go <a href="/resend">here</a> to get a new link sent ' +
             'to your email.'])
        
        # Activate user and try logging in again
        self.activate_user(user)
        response = self.client.post('/login', fields, follow=True)
        self.assertRedirects(response, '/mypage', 302, 200)
    
    ### Helpers ###
        
    def create_user(self):
        """
        Use the form to create a user and save it to the database
        """
        params = {
            'email':'test@test.com',
            'password1':'test',
            'password2':'test',
            'first_name':'Test',
            'last_name':'User',
            'fbid': -1
        }
        form = EmailUserCreationForm(params)
        user = form.save()
        # Check to make sure user creation worked
        self.assertIsNotNone(User.objects.get(email='test@test.com'))
        return user
    
    def activate_user(self, user):
        """
        Activate the given user
        """
        user.is_active = True
        user.save()



#try:
#    from selenium.webdriver.firefox.webdriver import WebDriver
#except:
#    print "You need to install Selenium WebDriver!!!"
#
#@override_settings(
#   EMAIL_HOST = 'localhost',
#   EMAIL_PORT = 1025,
#   EMAIL_HOST_USER = '',
#   EMAIL_HOST_PASSWORD = '',
#   WEB_ROOT = 'http://localhost:8081',
#   FACEBOOK_REDIRECT_URI = "http://localhost:8081/"
#)
#class MySeleniumTests(LiveServerTestCase):
#    fixtures = ['user-data.json']
#
#    @classmethod
#    def setUpClass(cls): 
#        cls.selenium = WebDriver()
#        super(MySeleniumTests, cls).setUpClass()
#
#    @classmethod
#    def tearDownClass(cls):
#        cls.selenium.quit()
#        super(MySeleniumTests, cls).tearDownClass()
#
#    def test_login(self):
#        from selenium.webdriver.support.wait import WebDriverWait
#        import time
#        
#        driver = self.selenium
#        
#        with self.settings(WEB_ROOT='http://localhost:8081'):
#            driver.get('%s%s' % (self.live_server_url, '/register'))
#        
#        timeout = 10        
#        WebDriverWait(driver, timeout).until(
#            lambda driver: driver.find_element_by_class_name("fb_ltr"))
#        
#        frame = driver.find_element_by_class_name("fb_ltr")
#        driver.switch_to_frame(frame)
#        
#        firstname_input = driver.find_element_by_name("first_name")
#        firstname_input.send_keys('Test')
#        lastname_input = driver.find_element_by_name("last_name")
#        lastname_input.send_keys('User')
#        email_input = driver.find_element_by_name("email")
#        email_input.send_keys('test@test.com')
#        
#        driver.find_element_by_class_name('fbRegistrationRegisterButton').click()
#    
#        time.sleep(4)
#        
#        alert = driver.switch_to_alert()
#        alert.accept()
#        
#        time.sleep(5)
