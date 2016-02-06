import time
from os.path import join
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from .base import FunctionalTest

class RegisteredUserInteractsWithLesson(FunctionalTest):
    
    def test_can_reach_lesson_from_course_page_and_see_resources(self):
        # Gaby visits and logs in to the site.
        self.browser.get(self.server_url)
        self._logUserIn('gaby','gaby5')
        
        # She returns to the homepage
        self.browser.find_element_by_id('id_homelink').click()
        
        # Navigates to the blender course home page
        fishing_course = self.browser.find_element_by_id('id_Blender_course')
        fishing_course.click()
        # She enrols on the course
        enrol = self.browser.find_element_by_id('id_enrol_button')
        enrol.click()
        
        # There are some lessons in the resource area
        lessons = self.browser.find_element_by_id('id_resource_lessons')
        self.assertGreaterEqual(
            len(lessons.find_elements_by_class_name('pure-paginator')),1)        
        
        # Gaby selects the first lesson and is taken to the lesson page
        self._expand_all_collapsible_blocks()
        lessons.find_element_by_id('id_lesson1').click()
        lesson_page_title = self.browser.find_element_by_id('id_lesson_title')
        self.assertEqual(
            lesson_page_title.text, "Lesson: What is Blender for?")
        
        # The breadcrumb trail updates to show her position on the first lesson 
        # of the course
        breadcrumb = self.browser.find_element_by_id('id_breadcrumb')
        self.assertEqual(breadcrumb.text, "All Courses > Blender Home > Lesson Home")
        
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
        self.assertTrue(resource_area.find_element_by_id('id_resource_LIs'))
        self.assertTrue(resource_area.find_element_by_id('id_resource_attachments'))
            
        # Gaby sees a number of learning intentions for the lesson 
        self.assertGreaterEqual(
            len(resource_area.find_element_by_id('id_resource_LIs').
            find_elements_by_tag_name('a')), 1)
                
    def test_can_reach_learning_intentions_and_browse_the_detail(self):
        """ From a lesson page, user can view the learning intentions and see
        the various success criteria etc."""
        
        # Gaby logs in, goes to the Blender course, lesson 1.
        # From there she selects the first learning intention link in the
        # learning intentions area.
        self.browser.get(self.server_url)
        self._logUserIn('gaby', 'gaby5')
        self.browser.find_element_by_id('id_homelink').click()
        self.browser.find_element_by_id('id_Blender_course').click()
        self.browser.find_element_by_id('id_lesson1').click()
        self.browser.find_element_by_id('id_resource_LIs').find_element_by_tag_name('a').click()
        
        # This takes her to a new page with the title 'Learning Intentions'
        self.assertIn(
            'Learning Intentions for Lesson',
            self.browser.find_element_by_id('id_title').text
        )
        
        # She notices that the menu entries update 
        self.assertIn('Blender Home', self.browser.find_element_by_id('menu').text)
        self.assertIn('Lesson Home', self.browser.find_element_by_id('menu').text)
        
        # ...and that the breadcrumb now shows the course > lesson > intention
        self.assertEqual(self.browser.find_element_by_id('id_breadcrumb').text,
        'All Courses > Blender Home > Lesson Home > Learning Intention')
        
        # The main resource area is split into 3 areas, consisting of 
        # 2 rows, where the second row has two equal columns.
        resource_area = self.browser.find_element_by_id('id_resource_area')
        LI_area = resource_area.find_element_by_id('id_resource_lint')
        LO_area = resource_area.find_element_by_id('id_resource_LO')
        SC_area = resource_area.find_element_by_id('id_resource_SC')
        self.assertEqual(SC_area.size['width'], LO_area.size['width'])

        # Gaby sees that the area at the top has detail of the learning 
        # intention.
        self.assertEqual(
            LI_area.find_element_by_tag_name('p').text,
            'Recognise a range of tasks for which Blender could be used'
        )
        # the left content area shows the related outcomes...
        LOs = LO_area.find_elements_by_class_name('learning_outcome')
        self.assertEqual(len(LOs), 2)
        self.assertEqual(
            LOs[0].text, 
            'I can correctly identify or reject various tasks as being well '\
            'suited to Blender'
        )
        # whilst the right area shows the related success criteria.
        SCs = SC_area.find_elements_by_class_name('criterion')
        self.assertEqual(len(SCs), 4)
        self.assertEqual(
            SCs[0].text, 
            'Spot 3D modelling tasks'
        )
        
    def test_cycle_learning_intention_details_user_enrolled(self):
        """See that the 'traffic light' device cycles properly"""

        # Gaby logs in to the site and heads to /lesson/1/lint/1
        self.browser.get(self.server_url)
        self._logUserIn('gaby', 'gaby5')
        self.browser.get(self.server_url+'/courses/1/')
        enrol = self.browser.find_element_by_id('id_enrol_button')
        enrol.click()
 
        self.browser.get(self.server_url+'/lesson/1/lint/1')
        
        # There she finds a traffic light device showing red status
        criterion = self.browser.find_element_by_xpath("//li[@class='criterion'][1]")
        device = self.browser.find_element_by_xpath("//li[@class='criterion'][1]/img")

        actions = ActionChains(self.browser)
        actions.double_click(device)
       
        self.assertEqual(criterion.text, u'Spot 3D modelling tasks')
        self.assertEqual(device.get_attribute('id'), u'id_SC1')
        self.assertEqual(
            device.value_of_css_property('background-position'), 
            u'0px 0px')
        self.assertTrue('tl-red' in device.get_attribute('class'))

        # (DBL)Clicking once, it changes to amber.
        actions.perform()
        time.sleep(0.1)
        self.assertEqual(
            device.value_of_css_property('background-position'),
            u'-17px 0px')
        self.assertTrue('tl-amber' in device.get_attribute('class'))

        # (DBL)Clicking again, the device changes to green.
        
        actions.perform()
        time.sleep(0.1)
        self.assertEqual(
            device.value_of_css_property('background-position'),
            u'-34px 0px')
        self.assertTrue('tl-green' in device.get_attribute('class'))

        # A further (DBL)click, cycles the device round to red again
        actions.perform()
        time.sleep(0.1)
        self.assertEqual(
            device.value_of_css_property('background-position'),
            u'0px 0px')
        self.assertTrue('tl-red' in device.get_attribute('class'))

    def test_peruse_lesson_when_not_enrolled(self):
        # Gaby knows that she can jump
        # directly to a lesson in one of the courses:
        self.browser.get(self.server_url)
        self._logUserIn('gaby', 'gaby5')
        self.browser.get(join(self.server_url,'courses/1/lesson/1/'))
        
        # She sees the site title, breadcrumb, and lesson title text
        self.assertEqual(self.browser.find_element_by_xpath("//div[@class='header']//h1").text, 'EduDuck')
        bc = self.browser.find_element_by_id('id_breadcrumb')
        bc.find_elements_by_tag_name('a')
        lt = self.browser.find_element_by_id('id_lesson_title')
        self.assertEqual(lt.text, 'Lesson: What is Blender for?')
        
        # Because she has not enrolled in this course, the Progress area
        # shows an 'enrol' button instead of any progress information.
        pa = self.browser.find_element_by_id('id_resource_progress')
        pa.find_element_by_id('id_enrol')

        # It's a free course so she enrols to gain access to subsequent lessons
        enrol = self.browser.find_element_by_id('id_enrol_button')
        enrol.click()
        # Gaby wishes to advance to the next lesson in the course. She does
        # so by clicking on the 'next lesson' navigation (back < curr > next)
        first_url = self.browser.current_url
        self.browser.find_element_by_id('id_nav_next').click()
        
        # The next lesson has a different url from the first
        second_url = self.browser.current_url
        self.assertNotEqual(first_url, second_url)
        # and Gaby sees that the lesson navigation updates to show links to 
        # both the previous lesson as well as a third lesson. 
        # The previous lesson link refers to the former url
        linkforw = self.browser.find_element_by_xpath(
            "//span/a[@id='id_nav_next']")
        linkback = self.browser.find_element_by_xpath(
            "//span/a[@id='id_nav_prev']")
        self.assertTrue('/courses/1/lesson/1' in linkback.get_attribute('href'))
        self.assertTrue('/courses/1/lesson/3' in linkforw.get_attribute('href'))

