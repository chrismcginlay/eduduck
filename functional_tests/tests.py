from unittest import skip
from registration.forms import RegistrationForm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class GeneralLayoutAndStyle(FunctionalTest):

    def test_basic_style(self):
        """The correct stylesheets and scripts are requested"""

        self.browser.get(self.server_url)
        style = """<link href="/static/index.css" rel="stylesheet" />"""
        self.assertIn(style, self.browser.page_source)
        
        style = """<link href="http://yui.yahooapis.com/pure/0.4.2/pure-min.css" rel="stylesheet" />"""
        self.assertIn(style, self.browser.page_source)
        
        style ="""<link href="/static/layouts/side-menu.css" rel="stylesheet" />"""
        self.assertIn(style, self.browser.page_source)
        
        script = """<script src="/static/js/ui.js">"""
        self.assertIn(script, self.browser.page_source)
        
        script = """<script src="http://code.jquery.com/ui/1.10.0/jquery-ui.js">"""
        self.assertIn(script, self.browser.page_source)
        
        script = "<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js\">"
        self.assertIn(script, self.browser.page_source)
        
class CasualVisitorArrives(FunctionalTest):

    def test_casual_visitor_arrives_on_site(self):
        """They should see the site title, list of existing courses,
        invitation to register/login, invitation to add courses"""

        # Nomski arrives on the site
        self.browser.get(self.server_url)

        # He sees the page title
        self.assertIn('EduDuck.com', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('EduDuck', header_text)

        # He sees the strapline
        strapline = self.browser.find_element_by_id('strapline').text
        self.assertIn('Courses are free to take\nor create your own.',
                      strapline)
        
        # Whilst the site is in development, he sees the current branch
        branch = self.browser.find_element_by_id('id_branch').text
        self.assertIn('Code Branch:', branch)

        # He sees facilities to register... (but doesn't, yet)
        self.assertTrue(self.browser.find_element_by_id('id_username'))
        self.assertTrue(self.browser.find_element_by_id('id_email'))
        self.assertTrue(self.browser.find_element_by_id('id_password1'))
        self.assertTrue(self.browser.find_element_by_id('id_password2'))
        self.assertTrue(self.browser.find_element_by_id('id_submit_reg'))

        # ...and the option to login, (but doesn't login)
        self.assertTrue(self.browser.find_element_by_id('id_login'))

        # He sees facilities to create a course
        self.assertTrue(self.browser.find_element_by_id('id_create_course'))
        
        # He sees a list of selected existing courses
        courses_area = self.browser.find_element_by_id('id_course_selection') 
        self.assertTrue(courses_area)
        # noticing there are 4 courses, and 'see all courses' too.
        courses = courses_area.find_elements_by_class_name('random_course')
        self.assertEqual(len(courses), 5)
        # ...with the specific option to list all courses
        self.assertTrue(self.browser.find_element_by_id('id_course_index'))

        #check element has minimum width and a colourful background
        for course in courses:
            self.assertGreaterEqual(course.size['width'], 50)
            back_color = course.value_of_css_property('background-color')
            self.assertNotEqual(back_color, 'transparent')

        see_all = self.browser.find_element_by_id('id_course_index')
        self.assertEqual(see_all.value_of_css_property('background-color'), u'rgba(192, 0, 0, 1)')

        # Finally, he notices the paypal button
        payarea = self.browser.find_element_by_id('id_paypal_button')
        target = 'https://www.paypal.com/cgi-bin/webscr'
        self.assertEqual(target, payarea.get_attribute('action'))

class CasualVisitorBrowsesMainMenu(FunctionalTest):
    
    def test_main_menu_items_present(self):
        # Heiko is visiting the site for the first time;
        # he checks out the main menu
        self.browser.get(self.server_url)
        menu = self.browser.find_element_by_id('menu')
        items_expected = ['Courses', 'Login', 
                          'Support', 'Contact', 'About']
        anchors = menu.find_elements_by_tag_name('a')
        a_list = [a.text for a in anchors]
        for item in items_expected:
            try:
                self.assertTrue(item in a_list)
            except:
                print "{0} not in menu".format(item)
                raise
                
    def test_main_menu_redirections(self):
        # Heiko is quite methodical and so works his way through each of the
        # main options in turn.
        
        self.browser.get(self.server_url)
        ##initially, I obtained the anchors outside the loop, however they go
        ##stale after browser back button. Hence the clunky loop index approach.
        number_of_anchors = len(self.browser.find_element_by_id('menu').find_elements_by_tag_name('a'))
        for i in range(number_of_anchors):
            start_window = self.browser.current_window_handle
            anchor = self.browser.find_element_by_id('menu').find_elements_by_tag_name('a')[i]
            url = anchor.get_attribute('href')
            anchor.click()
            ##Next get handle to opened window and switch to it
            open_windows = self.browser.window_handles
            self.browser.switch_to_window(open_windows[-1])
            self.assertEqual(url, self.browser.current_url)
            self.assertNotIn('Page Not Found', self.browser.title)
            self.assertNotIn('Page not found', self.browser.title)
            self.browser.back()
            self.browser.switch_to_window(start_window)
            if len(open_windows)>1:
                self.browser.close()  #close extra windows

class NewVisitorDecidesToRegister(FunctionalTest):
    """Covers registration, bio page, logout and login"""
    
    def test_registration_bio_edit_logout_login(self):
        # Roland arrives on the site. He has not registered yet.
        # He sees the login option in the menu and the registration area on the 
        # main page.
        self.browser.get(self.server_url)
        self.assertTrue(self.browser.find_element_by_id('id_login'))
        self.assertTrue(self.browser.find_element_by_id('id_sign_up_form'))

        # Roland is so keen to register, he accidentally hits 'sign up'
        # without first entering a username
        signup_form = self.browser.find_element_by_id('id_sign_up_form')
        signup_form.submit()
        
        # He is taken to the accounts/register page & an error message appears:
        error = self.browser.find_element_by_css_selector('.errorlist')
        self.assertEqual(error.text, "This field is required.")

        # Roland now fills in a username and clicks 'Sign Up' button
        signup_form = self.browser.find_element_by_tag_name('form')
        username_textarea = signup_form.find_element_by_id('id_username')
        username_textarea.send_keys("Roland")
        ## Seems to be necessary to refind form (goes out of cache?)
        signup_form = self.browser.find_element_by_tag_name('form')
        signup_form.submit()

        # Since he didn't fill in an email address or password, the form is 
        # re-presented with the same username, but the error fields highlighted.
        username_textarea = self.browser.find_element_by_id('id_username')
        self.assertEqual(username_textarea.get_attribute('value'), "Roland")
        errors = self.browser.find_elements_by_css_selector('.errorlist')
        self.assertEqual(len(errors), 3) #There are 3 blank fields so far

        for error in errors:
            self.assertEqual(error.text, "This field is required.")
        
        # He enters email and password details, 
        email_textarea = self.browser.find_element_by_id('id_email')
        password1_textarea = self.browser.find_element_by_id('id_password1')
        password2_textarea = self.browser.find_element_by_id('id_password2')
        email_textarea.send_keys('roland@example.com')
        password1_textarea.send_keys('wibble')
        password2_textarea.send_keys('wibble')
        
        # He re-submits the form, which passes validation. 
        # He is taken to the pending activation holding page_source
        signup_form = self.browser.find_element_by_tag_name('form')
        signup_form.submit()
        self.assertEqual(
            self.browser.current_url, 
            self.server_url + '/accounts/register/complete/')
        
        ## TODO The following would be nice to test. Need to figure out how to
        ## mock the confirmation email activation code.
        
"""
        # Roland is taken to his new user profile ('bio') page. 
        # Here he sees the basic and extra details for his account...
        self.assertEqual(self.browser.current_url, '/bio/views/edit')

        # ...including his gravatar...
        self.fail("write me")
        
        # ...and with the possibility to change the default timezone, tagline etc.
        detail_edit_form = self.browser.find_element_by_id('id_edit_account')
        self.assertTrue(detail_edit_form)
        
        # The main page no longer shows the registration area
        self.fail("write me")
        
        # After spending some time on the site, he decides revisit the account page
        pass

        # ...which shows up just fine
        self.fail("write me")

        # After spending some more time on the site, he then logs out.
        pass

        # The menu entry reverts to 'login' and the register area appears again.
        self.fail("write me")
        
        # Roland decides to login again. Pressing the login button, he is taken to
        # the login page
        self.fail("write me")
        
        # He logs in successfully and is taken to the home page.
        self.fail("write me")
"""

class RegisteredUserLogsIn(FunctionalTest):
    """ Covers the login/logout process """

    def test_login_logout(self):
        # Chris visits the site (cue music)
        self.browser.get(self.server_url)
        
        # He is not logged in, so sees the login option in the menu
        login_link = self.browser.find_element_by_id('id_login')
        self.assertTrue(login_link)
        
        import pdb; pdb.set_trace()
        # On clicking the login link, he is taken to the login page
        login_link.find_element_by_tag_name('a').click()
        self.assertEqual(
            self.browser.current_url, 
            self.server_url + '/accounts/login/')

        # Entering his username and password, he hits login
        username_textarea = self.browser.find_element_by_id('id_username')
        password_textarea = self.browser.find_element_by_id('id_password')
        form = self.browser.find_element_by_tag_name('form')
        username_textarea.send_keys('chris')
        password_textarea.send_keys('chris')
        form.submit()
        
        #This takes him to his account area
        self.assertEqual(self.browser.current_url,
                        self.server_url + '/bio/views/edit')
        
        # Since he is logged in, the menu now shows 'logout' in place of login. 
        self.assertFalse(self.browser.find_element_by_id('id_login'))
        self.assertTrue(self.browser.find_element_by_id('id_logout'))        
        
        # Also, a link to his 'account', including a small gravatar image
        account_link = self.broswer.find_element_by_id('id_account')
        self.assertTrue(account_link)
        account_alttext = account_link.get_attribute('alt')
        self.assertEqual(account_alttext, "Roland\'s Gravatar")
        self.assertTrue(self.broswer.find_element_by_id('id_gravatar'))

class AuthorCreatesMaterials(FunctionalTest):

    def test_can_create_course_and_retrieve_it_later(self):
        # Jules visits eduduck.com
        self.browser.get(self.server_url)

        # She logs in to the site...
        self.fail("Write me")

        # ...and is taken to her profile dashboard

        # There a text-box invites her to create a new course.

        # She calls her new course on 'Camping'...
        # ...and on pressing the add button is presented with a form to fill
        # The form automatically shows the course name 'Camping' and assigns
        # Jules as both organiser and author. She is asked to enter a summary,
        # a course code, level and number of credits.
        # On completing and submitting the form, the course is created in the
        # database, she is then taken to a new URL with all the fields
        # re-presented to her. She notices that there is an 'edit' button next
        # to each field and a button for adding lessons to the course.

        # She decides to alter the level from 'Intermediate' to 'Beginner'

        # Before Jules has time to add lessons, she has to go out, so logs out.

        # Later she returns to the site, logs in and immediately sees her new
        # course listed in her profile area. Happy days.

        # There is still a textbox for adding another course. She adds a course
        # on 'Mountain First Aid' but leaves the details blank for now.

        # Instead she returns to the profile page, where now both courses are
        # listed.
        # Now a new user, Albert, comes along to the site
        self.browser.quit()

        ## Clean browser instance - no cookie data etc.
        self.browser = webdriver.Firefox()

        # Albert visits the homepage. He sees both of Jules' courses under
        # 'available courses' but cannot edit them.
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Camping', page_text)
        self.assertIn('Mountain First Aid', page_text)

        # Albert now logs in and again sees both courses under 'available'
        # in his profile area. He enrols in 'Camping' and is taken to a new URL

        # This shows a list of lessons in the Camping course (currently zero)

        # He returns to his profile area and is pleased to see the Camping
        # course listed under 'Your Courses' and the first aid one still under
        # 'available'

        # Even though he is logged in, no edit facility is presented to Albert.

    def test_can_create_and_retrieve_lessons_associated_with_course(self):
        self.fail("Write test")

    def test_can_edit_course_populating_with_resources(self):
        """Author is able to create attachments, videos, LOs etc for course"""

        self.fail("Write test")

    def test_can_edit_lesson_populating_with_resources(self):
        """Author can create attachments, videos, LOs etc for lesson"""

        self.fail("Write test")

class PunterInteractsWithCourse(FunctionalTest):

    def test_punter_can_register_and_have_progress_logged(self):
        self.fail("Write test")

    def test_punter_can_complete_or_withdraw_from_course(self):
        self.fail("Write test")
