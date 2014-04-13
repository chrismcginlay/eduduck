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
        invitation to register, invitation to add courses"""

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

        # He sees facilities to register (but doesn't, yet)
        self.assertTrue(self.browser.find_element_by_id('id_username'))
        self.assertTrue(self.browser.find_element_by_id('id_email'))
        self.assertTrue(self.browser.find_element_by_id('id_password1'))
        self.assertTrue(self.browser.find_element_by_id('id_password2'))
        self.assertTrue(self.browser.find_element_by_id('id_submit_reg'))

        # He sees facilities to create a course
        self.assertTrue(self.browser.find_element_by_id('id_create_course'))

        # ...and an option to list all courses
        self.assertTrue(self.browser.find_element_by_id('id_course_index'))

        # He sees a list of selected existing courses
        courses_area = self.browser.find_element_by_id('id_course_selection') 
        self.assertTrue(courses_area)
        # noticing there are 4 courses...
        courses = courses_area.find_elements_by_class_name('random_course')
        self.assertEqual(len(courses), 4)

        import pdb; pdb.set_trace()
        #check element has minimum width and a colourful background
        for course in courses:
            self.assertGreaterEqual(course.size['width'], 50)
            back_color = course.value_of_css_property('background-color')
            self.assertEqual(back_color, 'rgba(200, 0, 0, 1)')

        # Finally, he notices the paypal button
        payarea = self.browser.find_element_by_id('id_paypal_button')
        target = 'https://www.paypal.com/cgi-bin/webscr'
        self.assertEqual(target, payarea.get_attribute('action'))

class NewVisitorDecidesToRegister(FunctionalTest):
    pass

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
