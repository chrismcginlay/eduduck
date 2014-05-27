from os.path import join
from unittest import skip
from selenium import webdriver

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
        
    @skip("Not implemented yet")
    def test_user_can_see_information_on_video_page(self):
        # Marek visits the page for the first video
        self.fail("Navigate to the video")

        ##Temporarily jump right in
        self.browser.get(join(self.server_url, '/video/1'))

        # Marek sees the title of the video, along with the video itself
        self.fail("write me")
        
        # Beneath that (since he is logged in) he sees a record of the number
        # of viewings of the video he has made.
        
        # Lastly, there is an area for him to enter his own notes on the video
        
        # When he navigates away from the page, and returns to the video page,
        # he is pleased to see that his notes are still there.

