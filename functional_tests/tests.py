from unittest import skip
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

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
        self.assertIn("Courses are free to make\nif they're free to take.",
                      strapline)
        
        # Whilst the site is in development, he sees the current branch
        branch = self.browser.find_element_by_id('id_branch').text
        self.assertIn('Code Branch:', branch)

        # He sees facilities to register... (but doesn't, yet)
        self.assertTrue(self.browser.find_element_by_id('id_sign_up_form'))
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
        courses_area_pixel_width = courses_area.size['width']
        
        self.assertTrue(courses_area)
        # noticing there are up to 6 courses, and 'see all courses' too.
        courses = courses_area.find_elements_by_class_name('random_course')
        self.assertLessEqual(len(courses), 7)
        # ...with the specific option to list all courses
        self.assertTrue(self.browser.find_element_by_id('id_course_index'))

        # checking element has appropriate width and a colourful background
        for course in courses:
            back_color = course.value_of_css_property('background-color')
            self.assertNotEqual(back_color, 'transparent')
    
        ## Group courses in 3s, divide widths into w 24ths proportional to 
        ## length of course name. NB that the 'see all courses' entry doesn't 
        ## get counted as it gets a row on its own (the last 'course')
        real_courses = courses[:-1]
        for i in [3*j for j in range(1+min(len(real_courses)-1,6)/3)]: #[0,3,6...]
            c0,c1,c2 = (0,0,0)
            try:
                c0 = len(real_courses[i+0].text)
                c1 = len(real_courses[i+1].text)
                c2 = len(real_courses[i+2].text)
            except IndexError:
                pass
            c_total = c0+c1+c2
            w0 = int(24*c0/c_total)
            w1 = int(24*c1/c_total)
            w2 = 24-w0-w1
            #Adjust w0,w1 to ensure total 24 if only 1 or 2 courses in row:
            if c1==0: (w0,w1,w2)=(24,0,0)
            if c2==0: (w1,w2)=(24-w0,0)
            capw = courses_area_pixel_width
            if w0: self.assertEqual(round(24*float(real_courses[i+0].size['width'])/capw), w0)
            if w1: self.assertEqual(round(24*float(real_courses[i+1].size['width'])/capw), w1)
            if w2: self.assertEqual(round(24*float(real_courses[i+2].size['width'])/capw), w2)

        see_all = self.browser.find_element_by_id('id_course_index')
        self.assertEqual(see_all.value_of_css_property('background-color'), u'rgba(192, 0, 0, 1)')

        # The footer area shows the current year in the copyright notice
        thisyear = datetime.now().year
        footeryear = self.browser.find_element_by_id('id_pagefoot').text.split(' ')[2]
        self.assertEqual(int(footeryear), thisyear)
        
        # Finally, he notices the paypal button
        payarea = self.browser.find_element_by_id('id_paypal_button')
        target = 'https://www.paypal.com/cgi-bin/webscr'
        self.assertEqual(target, payarea.get_attribute('action'))

class VisitorBrowsesMenus(FunctionalTest):
    
    def test_main_menu_items_not_logged_in(self):
        # Urvasi is visiting the site for the first time;
        # She checks out the main menu
        self.browser.get(self.server_url)
        items_expected = [
            'Courses', 'Login', 'Register', 
            'Blog', 'Support', 'About']
        self._checkChildItemsPresent(items_expected, 'menu')

        # Urvasi is quite methodical and so works her way through each of the
        # main options in turn.
        self._checkChildLinksWork('menu')
        
    def test_main_menu_items_logged_in(self):
        # Urvasi decides to login, whereupon she notices that the menu options
        # have changed a little
        self.browser.get(self.server_url)
        self._logUserIn('urvasi', 'hotel23')
        ##check logout last as clicking it has a side-effect.
        items_expected = [
            'Courses', 'Urvasi', 'Blog', 
            'Support', 'About', 'Logout']
        self._checkChildItemsPresent(items_expected, 'menu')
        self._checkChildLinksWork('menu')
        
    def test_course_menu_items_logged_in(self):
        # She then goes to one of the course pages
        self.browser.get(self.server_url)
        self._logUserIn('urvasi', 'hotel23')
        self.browser.find_element_by_id('id_homelink').click()
        self.browser.find_element_by_id('id_ISS_course').click()

        # and notes that the menu changes slightly in the course context
        items_expected = ['Urvasi', 'ISS', 'Intro Videos', 'Lessons', 
            'Assessments', 'Study Group', 'Course Docs', 'Progress'
        ]
        self._checkChildItemsPresent(items_expected, 'menu')
        self._checkChildLinksWork('menu')
        
    def test_lesson_menu_items_logged_in(self):
        # Urvasi now visits a lesson within one of the courses and sees menu
        # items relevant to the lesson context
        self.browser.get(self.server_url)
        self._logUserIn('urvasi', 'hotel23')
        self.browser.find_element_by_id('id_homelink').click()
        self.browser.find_element_by_id('id_ISS_course').click()
        self.browser.find_element_by_id('id_lesson1').click()
        items_expected = ['Urvasi', 'ISS Home', 'Lesson Home', 'Learn.. Int..',
                          'Assessment', 'Study Group', 'Docs', 'Progress'
        ]
        self._checkChildItemsPresent(items_expected, 'menu')
        self._checkChildLinksWork('menu')

    def test_LI_menu_items_logged_in(self):
        # Next, Urvasi drills into the learning intentions page and again
        # sees the menu options change slightly.
        self.browser.get(self.server_url)
        self._logUserIn('urvasi', 'hotel23')
        self.browser.find_element_by_id('id_homelink').click()
        self.browser.find_element_by_id('id_Blender_course').click()
        self.browser.find_element_by_id('id_lesson1').click()
        self.browser.find_element_by_id('id_LI1').click()
        items_expected = ['Blender Home', 'Lesson Home', ]
        self._checkChildItemsPresent(items_expected, 'menu')
        self._checkChildLinksWork('menu')
        
class VisitorBrowsesBreadcrumbs(FunctionalTest):
    
    def test_breadcrumb_trail_for_course_lesson_lint(self):
        # Helmi navigates to a course page
        # She sees a breadcrumb trail beginning near the top of the content
        # At this stage, it can only take her back to the index or course page
        self.browser.get(self.server_url)
        self._logUserIn('helmi', 'plate509')
        self.browser.find_element_by_id('id_homelink').click()
        self.browser.find_element_by_id('id_Blender_course').click()
        items_expected = ['All Courses', 'Blender Home']
        self._checkChildItemsPresent(items_expected, 'id_breadcrumb')
        self._checkChildLinksWork('id_breadcrumb')
                
        # Back on a course page, Helmi navigates to a lesson
        self.browser.find_element_by_id('id_lesson1').click()

        # Now, the breadcrumb trail extends, with an additional link back to 
        # the selected course and to the top of the lesson
        items_expected = ['All Courses', 'Blender Home', 'Lesson Home']
        
        # She tests this link, which works, then returns to the lesson page.
        self._checkChildItemsPresent(items_expected, 'id_breadcrumb')
        self._checkChildLinksWork('id_breadcrumb')
        
        # Further down the lesson page, Helmi sees the learning intentions area.
        # On selecting one of the LIs, she finds that the LI page's breadcrumb
        # extends yet again, this time adding a link to the lesson page.
        self.browser.find_element_by_id('id_LI1').click()
        items_expected = [
            'All Courses', 
            'Blender Home', 
            'Lesson Home', 
            'Learning Intention'
        ]
        self._checkChildItemsPresent(items_expected, 'id_breadcrumb')
        
        # This link also works.
        self._checkChildLinksWork('id_breadcrumb')
        
            

