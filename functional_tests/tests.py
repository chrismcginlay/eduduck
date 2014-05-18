from datetime import datetime
from unittest import skip
from registration.forms import RegistrationForm
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
        self.assertIn('Courses are free to take\nor create your own.',
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
        items_expected = ['Courses', 'Login', 'Register', 
                          'Support', 'About']
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
        items_expected = ['Courses', 'Urvasi', 'Support', 'About', 'Logout']
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
        # Helmi navigates to a course page_source
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
        # Use a public mailinator address to get the activation code
        email_textarea.send_keys('rolandtheeduducker@mailinator.com')
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
        ## Could use mailinator or filebased backend for email.
        
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
        self.loguserin('Roland', 'wibble')
        
        # He logs in successfully and is taken to the home page.
        self.fail("write me")
"""

class RegisteredUserLogsIn(FunctionalTest):
    """ Covers the login/logout process """

    def test_login_logout(self):
        # Chris visits the site (cue music)
        self.browser.get(self.server_url)

        # He is not logged in, so sees the login option in the menu
        self.loguserin('chris', 'chris')

        #This takes him to his account area
        self.assertEqual(
            self.browser.current_url,
            self.server_url + '/accounts/bio/')

        # Since he is logged in, the menu now shows 'logout' in place of login. 
        try:
            self.browser.find_element_by_id('id_login')
        except NoSuchElementException:
            pass
        self.assertTrue(self.browser.find_element_by_id('id_logout'))        

        # Also, a link to his 'account', including a small gravatar image
        account_link = self.browser.find_element_by_id('id_account')
        self.assertTrue(account_link)
        gravatar = self.browser.find_element_by_id('id_gravatar')
        self.assertEqual(gravatar.get_attribute('alt'), "Chris\'s gravatar")


class RegisteredUserInteractsWithCourse(FunctionalTest):

    def test_user_enrols_on_course(self):
        # User Chris logs in.
        self.browser.get(self.server_url)
        self.loguserin('chris', 'chris')
        
        # he goes back to the homepage
        self.browser.find_element_by_id('id_homelink').click()
        
        # Given that he has not registered on any courses, the homepage shows
        # a selection of courses.
        courses_area = self.browser.find_element_by_id('id_course_selection') 

        
        # He selects the Fishing course and is taken to that course's homepage
        # where he can view an intro video, see an invitation to enrol
        # see a list of lessons, assessments and resources in the main course
        # resource area

        fishing_course = self.browser.find_element_by_id('id_Fishing_course')
        fishing_course.click()
        self.assertTrue(self.browser.find_element_by_id('id_course_title'))
        enrol = self.browser.find_element_by_id('id_enrol')
        course_intro = self.browser.find_element_by_id('id_course_intro_area')
        self.assertTrue(course_intro.find_element_by_id('id_abstract'))
        self.assertTrue(course_intro.find_element_by_tag_name('iframe'))
        resource_area = self.browser.find_element_by_id('id_resource_area')
        self.assertTrue(resource_area.find_element_by_id('id_resource_lessons'))
        self.assertTrue(resource_area.find_element_by_id('id_resource_assessments'))
        self.assertTrue(resource_area.find_element_by_id('id_resource_attachments'))
        self.assertTrue(resource_area.find_element_by_id('id_resource_study'))

        # He notices further down the page, that the 'Progress' area offers 
        # yet another opportunity to enrol on the course.
        progress = resource_area.find_element_by_id('id_resource_progress')
        progress.find_element_by_id('id_enrol_x2')
        
        # On enrolling the page reloads and a welcome message appears in the 
        # progress area, instead of the enrol button
        enrol.click()
        resource_area = self.browser.find_element_by_id('id_resource_area')
        progress = resource_area.find_element_by_id('id_resource_progress')
        try:
            progress.find_element_by_id('id_enrol_x2')
        except:
            pass
        self.assertEqual(progress.find_element_by_tag_name('h3').text, "Your Progress")
        
        # Also, on investigating the site menu, he notices that new options
        # are there for the fishing home, lessons, assessments
        menu = self.browser.find_element_by_id('menu')
        items_expected = ['Fishing Home', 'Lessons', 'Assessments', 'Forum',
                          'Study Group', 'Logout', 'Support', 'Contact', 'About']
        anchors = menu.find_elements_by_tag_name('a')
        a_list = [a.text for a in anchors]
        for item in items_expected:
            try:
                self.assertTrue(item in a_list)
            except:
                print "{0} not in menu".format(item)
                raise
        
        # On the course homepage, Chris also sees buttons to withdraw from the 
        # course or to mark it as 'complete'.
        progress.find_element_by_id('id_withdraw')
        progress.find_element_by_id('id_complete')
        
    def test_user_can_complete_or_withdraw_from_course(self):
        self.fail("Write test")


class RegisteredUserInteractsWithLesson(FunctionalTest):
    
    def test_can_reach_lesson_from_course_page_and_see_resources(self):
        # Gaby visits and logs in to the site.
        self.browser.get(self.server_url)
        self.loguserin('gaby','gaby5')
        
        # She returns to the homepage
        self.browser.find_element_by_id('id_homelink').click()
        
        # Navigates to the blender course home page
        fishing_course = self.browser.find_element_by_id('id_Blender_course')
        fishing_course.click()
        
        # She enrols on the course
        enrol = self.browser.find_element_by_id('id_enrol')
        enrol.click()
        
        # There are some lessons in the resource area
        lessons = self.browser.find_element_by_id('id_resource_lessons')
        self.assertGreaterEqual(
            len(lessons.find_elements_by_class_name('paginator')),1)        

        # Gaby selects the first lesson and is taken to the lesson page
        lessons.find_element_by_class_name('paginator').click()
        lesson_page_title = self.browser.find_element_by_id('id_lesson_title')
        self.assertEqual(
            lesson_page_title.text, "Lesson BL1: What is Blender for?")
        
        # The breadcrumb trail updates to show her position on the first lesson 
        # of the course
        breadcrumb = self.browser.find_element_by_id('id_breadcrumb')
        self.assertEqual(breadcrumb.text, "All Courses > Blender > What is Blender?")
        
        # Just under the breadcrumb, there is a tool to navigate between lessons
        self.assertTrue(self.browser.find_element_by_class_name('prev_next'))
    
        # The main body of the lesson page shows the video, attachment and 
        # learning outcomes in the main lesson resource area
        self.assertTrue(self.browser.find_element_by_id('id_lesson_title'))
        lesson_intro = self.browser.find_element_by_id('id_lesson_intro_area')
        self.assertTrue(lesson_intro.find_element_by_id('id_abstract'))

        resource_area = self.browser.find_element_by_id('id_resource_area')
        ##videos are iframes for YouTube, if videos are present:
        resource_videos = resource_area.find_element_by_id('id_resource_videos')
        try:
            self.assertTrue(resource_videos.find_element_by_tag_name('iframe'))
        except:
            self.assertEqual(
                resource_videos.find_element_by_tag_name('li').text,
            'No videos for this lesson')
        self.assertTrue(resource_area.find_element_by_id('id_resource_survey'))
        self.assertTrue(resource_area.find_element_by_id('id_resource_progress'))
        self.assertTrue(resource_area.find_element_by_id('id_resource_learning_intentions'))
        self.assertTrue(resource_area.find_element_by_id('id_resource_attachments'))
        
        # Gaby sees a number of learning intentions for the lesson 
        self.assertGreaterEqual(
            len(resource_area.find_element_by_id('id_resource_learning_intentions').
            find_elements_by_tag_name('a')), 1)
            
        
    def test_can_reach_learning_intentions_and_browse_the_detail(self):
        """ From a lesson page, user can view the learning intentions and see
        the various success criteria etc."""
        
        # Gaby logs in, goes to the Blender course, lesson 1.
        # From there she selects the first learning intention link in them
        # learning intentions area.
        self.browser.get(self.server_url)
        self.loguserin('gaby', 'gaby5')
        self.browser.find_element_by_id('id_homelink').click()
        self.browser.find_element_by_id('id_Blender_course').click()
        self.browser.find_element_by_id('id_enrol').click()
        self.browser.find_element_by_class_name('paginator').click()
        self.browser.find_element_by_id('id_resource_learning_intentions').find_element_by_tag_name('a').click()
        
        # This takes her to a new page with the title 'Learning Intentions'
        self.assertEqual(self.browser.find_element_by_id('id_title'), 
                         'Learning Intention for Lesson ...')
        
        # She notices that the menu entries update 
        self.assertIn(self.browser.find_element_by_id('id_menu').text, 'Blender')
        self.assertIn(self.browser.find_element_by_id('id_menu').text, 'Lesson 1')
        
        # ...and that the breadcrumb now shows the course > lesson > intention
        self.assertEqual(self.browser.find_element_by_id('id_breadcrumb'),
                         'All Courses > Blender > Rods > Learning Intentions')
        
        # The main resource area is split into 3 areas, consisting of 
        # 2 columns, where the second column has two rows, like: OB
        resource_area = self.browser.find_element_by_id('id_resource_area')
        LI_area = resource_area.find_element_by_id('id_resource_LIs')
        LO_area = resource_area.find_element_by_id('id_resource_LO')
        SC_area = resource_area.find_element_by_id('id_resource_SC')
        self.assertEqual(LI_area.size['width'], LO_area.size['width'])
        self.assertEqual(LO_area.size['height'], SC_area.size['height'])
        
        # Gaby sees that the larger area on the left has a list of learning 
        # intentions, with a clickable icon next to each.
        
        # On clicking the first icon, some detail of the learning intention 
        # expands vertically and...
        
        # the top right content area shows the related outcomes...
        
        # whilst the bottom right area shows the related success criteria.
        
        # Gaby clicks on another intention, which expands as the old one 
        # collapses...
        
        # ...and the right hand areas show the relevant outcomes/criteria.
        self.fail("write me")
        
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

