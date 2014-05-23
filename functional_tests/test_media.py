from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class VideoIntegration(FunctionalTest):

    def test_course_and_lesson_page_can_show_videos(self):
        # A user, let's call him Marek, hits the homepage and navigates to the
        # first course
        self.browser.get(self.server_url)
        self.browser.find_element_by_xpath("//div[@id='id_course_selection']/div[1]/a").click()

        # At this point he can see an embedded intro video 
        # (probably outlining the course)
        self.browser.find_element_by_xpath("//div[@id='id_intro_video']/iframe")
        
        # as well as further video embedded down the page 
        # (including the intro video)
        self.browser.find_element_by_xpath("//div[@id='id_resource_videos']/iframe")
        
        # Having explored the course page, Marek visits the first lesson:
        self.browser.find_element_by_id("id_lesson1").click()
        
        # On the lesson page, there is a video section with video ready to see
        video_area = self.browser.find_element_by_xpath("//div[@id='id_resource_videos']")
        self.assertEqual(video_area.find_element_by_tag_name('h3').text, "Videos")
        video_area.find_element_by_tag_name("iframe")
        
    def test_user_can_see_information_on_video_page(self):
        self.fail("write me")

@skip("")
class AttachmentIntegration(FunctionalTest):
    
    pass
