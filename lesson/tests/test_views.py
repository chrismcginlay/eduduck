# lesson/tests/test_views.py

from datetime import datetime
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http.response import HttpResponseForbidden
from django.test import TestCase
from django.utils.html import escape
from django.utils.timezone import utc

from checkout.models import Payment, PricedItem
from courses.models import Course
from lesson.models import Lesson
from interaction.models import UserCourse
from attachment.forms import (
    ATTACHMENT_NAME_FIELD_REQUIRED_ERROR,
    ATTACHMENT_ATTACHMENT_FIELD_REQUIRED_ERROR,
)
from video.forms import (
    VIDEO_NAME_FIELD_REQUIRED_ERROR,
    VIDEO_URL_FIELD_INVALID_ERROR,
)
from ..forms import (
    LESSON_NAME_FIELD_REQUIRED_ERROR,
    LESSON_ABSTRACT_FIELD_REQUIRED_ERROR,
    )
from ..views import (
    _user_can_view_lesson,
    LessonEditForm,
    VideoInlineFormset,
    AttachmentInlineFormset,
    LearningIntentionInlineFormset,
    )


class LessonViewTests(TestCase):
    
    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
        ]
  
    def test__user_can_view_lesson_Always_allows_lesson_1(self):
        course = Course.objects.get(pk=1)
        lessons = course.lesson_set
        first_lesson = lessons.first()
        # Gaby hasn't paid, but can still view the first lesson
        user = User.objects.get(pk=3) # gaby in fixture
        self.client.login(username=user.username, password='gaby5')        
        self.assertTrue(_user_can_view_lesson(user, first_lesson))

    def test__user_can_view_lesson_Always_allows_instructor(self):
        """Instructor/organiser can view all lessons on course"""
        course = Course.objects.get(pk=1)
        lessons = course.lesson_set
        instructor = course.instructor
        organiser = course.organiser
        user = User.objects.get(pk=6)
        self.client.login(username=user.username, password='helen')
        second_lesson = lessons.first().get_next()
        self.assertTrue(_user_can_view_lesson(user, second_lesson))
 
    def test__user_can_view_lesson_Always_allows_organiser(self):
        """Instructor/organiser can view all lessons on course"""
        course = Course.objects.get(pk=1)
        lessons = course.lesson_set
        instructor = course.instructor
        organiser = course.organiser
        user = User.objects.get(pk=7)
        self.client.login(username=user.username, password='sven')
        second_lesson = lessons.first().get_next()
        self.assertTrue(_user_can_view_lesson(user, second_lesson))

    def test__user_can_view_lesson_Checks_paid_status(self):
        lesson = Lesson.objects.get(pk=2)
        lesson_url = lesson.get_absolute_url

        # Gaby hasn't paid
        user = User.objects.get(pk=3) # gaby in fixture
        self.client.login(username=user.username, password='gaby5')        
        self.assertFalse(_user_can_view_lesson(user, lesson))

        # Urvasi has paid
        user = User.objects.get(pk=4)
        current_time = datetime.utcnow().replace(tzinfo=utc)
        payment = Payment(
            paying_user=user,
            content_object=lesson.course,
            fee_value=1,
            datestamp=current_time,
        )
        payment.save()
        self.client.login(username=user.username, password='hotel23')        
        self.assertTrue(_user_can_view_lesson(user, lesson))

    def test__user_can_view_lesson_Returns_true_if_duplicate_payments(self):
        """Duplicate payments shouldn't occur, but if they do the user
        should be able to view the lesson"""

        lesson = Lesson.objects.get(pk=2)
        # Urvasi has paid twice
        user = User.objects.get(pk=4)
        current_time = datetime.utcnow().replace(tzinfo=utc)
        payment = Payment(
            paying_user=user,
            content_object=lesson.course,
            fee_value=1,
            datestamp=current_time,
        )
        payment.save()
        payment2 = Payment(
            paying_user=user,
            content_object=lesson.course,
            fee_value=1.1,
            datestamp=current_time,
        )
        payment2.save()
        self.client.login(username=user.username, password='hotel23')        
        self.assertTrue(_user_can_view_lesson(user, lesson))

    def test_lesson_visit_requires_payment(self):
        lesson = Lesson.objects.get(pk=2)
        lesson_url = lesson.get_absolute_url()
        course_url = lesson.course.get_absolute_url()
        # Gaby hasn't paid
        user = User.objects.get(pk=3) # gaby in fixture
        self.client.login(username=user.username, password='gaby5')        
        response = self.client.get(lesson_url)
        self.assertRedirects(response, course_url) 
        # Urvasi has paid
        user = User.objects.get(pk=4)
        current_time = datetime.utcnow().replace(tzinfo=utc)
        payment = Payment(
            paying_user=user,
            content_object=lesson.course,
            fee_value=1,
            datestamp=current_time,
        ).save()
        self.client.login(username=user.username, password='hotel23')        
        response = self.client.get(lesson_url)
        self.assertEqual(response.status_code, 200)

    def test_lesson_1_always_visible(self):
        lesson = Lesson.objects.get(pk=1)
        lesson_url = lesson.get_absolute_url()
        # Gaby hasn't paid
        user = User.objects.get(pk=3) # gaby in fixture
        self.client.login(username=user.username, password='gaby5')        
        response = self.client.get(lesson_url)
        self.assertEqual(response.status_code, 200)

    def test_lesson_unauth(self):
        """Test view of single lesson for unauthenticated user"""
        
        l1 = Lesson.objects.get(pk=1)
        url1 = l1.get_absolute_url()
        
        self.client.logout()
        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
                        for x in ['course', 'lesson', 'ul', 'attachments',
                        'history', 'learning_intentions'])
        self.assertEqual(response.context['history'], None, 
                        "There should be no history - unauthenticated")
        self.assertEqual(response.context['ul'], None, 
                        "There should be no userlesson - unauthenticated")                 
        self.assertNotIn('id_lesson_edit', response.content,
                        "There should be no edit button -unauthenticated")

    def test_lesson_loggedin_and_enrolled_on_course(self):

        user = User.objects.get(pk=3) # gaby in fixture
        self.client.login(username=user.username, password='gaby5')        
        l1 = Lesson.objects.get(pk=1)
        url1 = '/courses/{0}/lesson/{1}/'.format(l1.course.pk, l1.pk)

        # Enrol the user on the course
        uc = UserCourse(user=user, course=l1.course)
        uc.save()
        # Visit the page
        response = self.client.get(url1)
        
        self.assertIn('attachments', response.context, \
            "Missing template var: attachments")
        self.assertEqual(response.status_code, 200)

        hist = response.context['history'].pop()
        self.assertIsInstance(hist[0], datetime, 
                              "Problem with lesson history timestamp")
        self.assertEqual(hist[1], 'VISITING', 
                         "Problem with lesson history activity")
        
        self.assertNotEqual(response.context['ul'], None, 
                            "There should be a userlesson - authenticated")                 
        #see that lesson complete button works 
        response = self.client.post(url1, {'lesson_complete':'Complete'})
        self.assertIn('lesson_reopen', response.content)
        self.assertEqual(response.context['ul'].completed, True) 
        
        #see that lesson reopen button works 
        response = self.client.post(url1, {'lesson_reopen':'Re-open'})
        self.assertIn('lesson_complete', response.content)
        self.assertEqual(response.context['ul'].completed, False)        

    def test_lesson_loggedin_but_not_enrolled_on_course(self):
        user = User.objects.get(pk=4) # gaby in fixture
        self.client.login(username=user.username, password='hotel23')        
        l1 = Lesson.objects.get(pk=1)
        url1 = l1.get_absolute_url()

        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)
        self.assertIn('attachments', response.context, \
            "Missing template var: attachments")
        self.assertEqual(response.context['history'], None, 
                         "There should be no history - not enrolled")
        self.assertEqual(response.context['ul'], None, 
                         "There should be no userlesson - not enrolled")  

    def test_lesson_viewable_if_instructor_is_logged_in(self):
        """Instructor/organiser can view all lessons on course"""
        course = Course.objects.get(pk=1)
        lessons = course.lesson_set
        instructor = course.instructor
        organiser = course.organiser
        user = User.objects.get(pk=6)
        self.client.login(username=user.username, password='helen')
        second_lesson = lessons.first().get_next()
        response = self.client.get(second_lesson.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_lesson_viewable_if_organiser_is_logged_in(self):
        """Instructor/organiser can view all lessons on course"""
        course = Course.objects.get(pk=1)
        lessons = course.lesson_set
        instructor = course.instructor
        organiser = course.organiser
        user = User.objects.get(pk=7)
        self.client.login(username=user.username, password='sven')
        second_lesson = lessons.first().get_next()
        response = self.client.get(second_lesson.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_lesson_page_has_edit_button_for_organiser_instructor(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/1/lesson/1/')
        self.assertIn("id='id_edit_lesson'", response.content)
        self.assertEqual(response.context['user_can_edit_lesson'], True)

    def test_no_enrol_buttons_for_organiser_instructor(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/1/lesson/1/')
        self.assertNotIn('id_enrol_button', response.content)
        self.assertNotIn('id_enrol_button2', response.content)
        self.assertIn(
            'You are involved in running this course', response.content)

    def test_lesson_page_has_no_edit_buttons_if_not_organiser_instructor(self):
        self.client.login(username='helmi', password='plate509')
        response = self.client.get('/courses/1/lesson/1/')
        self.assertNotIn("id='id_edit_lesson'", response.content)
        self.assertNotIn("id='id_edit_lesson2'", response.content)
        self.assertEqual(response.context['user_can_edit_lesson'], False)

    def test_lesson_edits_actually_saved(self):
        self.client.login(username='helen', password='helen')
        fp = SimpleUploadedFile('atest.txt', 'A simple test file')
        mod_data = {
            'lesson_form-code': 'F1', 
            'lesson_form-name': 'New Lesson Name', 
            'lesson_form-abstract': 'A new abstract',
            'video_formset-0-url':'http://www.youtube.com/embed/EJiUWBiM8HE',
            'video_formset-0-name':'Cmdr Hadfield\'s Soda',
            'video_formset-TOTAL_FORMS':u'1',
            'video_formset-INITIAL_FORMS':u'0',
            'attachment_formset-0-name':'A test file',
            'attachment_formset-0-desc':'A description of a file',
            'attachment_formset-0-attachment':fp,
            'attachment_formset-TOTAL_FORMS':u'1',
            'attachment_formset-INITIAL_FORMS':u'0',
            'learning_intention_formset-TOTAL_FORMS':u'5',
            'learning_intention_formset-INITIAL_FORMS':u'0',
        }
 
        ##This should trigger modification of the lesson
        response = self.client.post('/courses/1/lesson/1/edit/', mod_data)
        
        ##Then visiting the lesson should reflect the changes
        response = self.client.get('/courses/1/lesson/1/')
        self.assertContains(response, 
            '<h3>New Lesson Name</h3>', html=True)
        self.assertContains(response, '<p>A new abstract</p>', html=True)
        self.assertIn(escape('Cmdr Hadfield\'s Soda'), response.content)
        
        ##There is a list of attachments
        self.assertIn('id_attachment_list', response.content) 
        self.assertIn('EJiUWBiM8HE', response.content) #youtube video
        self.assertIn('A test file', response.content)

    def test_lesson_edit_redirects_if_not_loggedin(self):
        response = self.client.get('/courses/1/lesson/1/edit/')  
        login_redirect_url = '/accounts/login/?next=/courses/1/lesson/1/edit/'
        self.assertRedirects(response, login_redirect_url, 302, 200)

    def test_lesson_edit_forbidden_if_user_not_permitted(self):
        self.client.login(username='helmi', password='plate509')
        response = self.client.get('/courses/1/lesson/1/edit/')
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_lesson_edit_200_if_user_permitted(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/1/lesson/1/edit/') 
        self.assertEqual(response.status_code, 200)

    def test_lesson_edit_page_has_correct_title_and_breadcrumb(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/1/lesson/1/edit/')
        needle = "<h2 id='id_page_title'>Editing: What is Blender for?</h2>"
        self.assertIn(needle, response.content)
        self.assertIn("<p id='id_breadcrumb'>", response.content)
        self.assertContains(
            response, 
            '<a href="/courses/">All Courses</a>',
            html=True)
        self.assertContains(
            response,
            '<a href="/courses/1/">Blender</a>',
            html=True)
        self.assertContains(
            response,
            '<a href="/courses/1/lesson/1/">What is Blender for?</a>',
            html=True)

    def test_lesson_edit_uses_correct_template(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/1/lesson/1/edit/') 
        self.assertTemplateUsed(response, 'lesson/lesson_edit.html')

    def test_lesson_edit_page_uses_correct_form(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/1/lesson/1/edit/')
        self.assertIsInstance(response.context['lesson_form'], LessonEditForm)

    def test_lesson_edit_page_uses_correct_formsets(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/1/lesson/1/edit/')
        self.assertIsInstance(
            response.context['video_formset'], VideoInlineFormset)
        self.assertIsInstance(
            response.context['attachment_formset'], AttachmentInlineFormset)
        self.assertIsInstance(
            response.context['learning_intention_formset'], 
            LearningIntentionInlineFormset
        )
        self.assertTrue(
            hasattr(response.context['video_formset'], 'management_form'))
        self.assertTrue(
            hasattr(response.context['attachment_formset'], 'management_form'))
        self.assertTrue(hasattr(
            response.context['learning_intention_formset'], 'management_form'))

    def test_lesson_edit_page_POST_uses_correct_formsets(self):
        self.client.login(username='sven', password='sven')
        mod_data = {
            'video_formset-TOTAL_FORMS':u'1',
            'video_formset-INITIAL_FORMS':u'0',
            'attachment_formset-TOTAL_FORMS':u'1',
            'attachment_formset-INITIAL_FORMS':u'0',
            'learning_intention_formset-TOTAL_FORMS':u'5',
            'learning_intention_formset-INITIAL_FORMS':u'0',
        }
        response = self.client.post('/courses/1/lesson/1/edit/', mod_data)
        self.assertIsInstance(
            response.context['video_formset'], VideoInlineFormset)
        self.assertIsInstance(
            response.context['attachment_formset'], AttachmentInlineFormset)
        self.assertIsInstance(
            response.context['learning_intention_formset'], 
            LearningIntentionInlineFormset
        )
        self.assertEqual(
            response.context['learning_intention_formset'].prefix,
            'learning_intention_formset'
        ) 
        self.assertTrue(
            hasattr(response.context['video_formset'], 'management_form'))
        self.assertTrue(
            hasattr(response.context['attachment_formset'], 'management_form'))
        self.assertTrue(hasattr(
            response.context['learning_intention_formset'], 'management_form'))

    def test_lesson_edit_page_validation_errors_sent_to_template(self):
        self.client.login(username='sven', password='sven')
        fp = SimpleUploadedFile('atest.txt', 'A simple test file')
        mod_data = {
            'lesson_form-code': '', 
            'lesson_form-name': '', 
            'lesson_form-abstract': '',
            'video_formset-0-url':'http://www.youtube.com/embed/E8HE',
            'video_formset-0-name':'',
            'video_formset-TOTAL_FORMS':u'1',
            'video_formset-INITIAL_FORMS':u'0',
            'attachment_formset-0-name':'',
            'attachment_formset-0-desc':'',
            'attachment_formset-0-attachment':fp,
            'attachment_formset-TOTAL_FORMS':u'1',
            'attachment_formset-INITIAL_FORMS':u'0',
            'learning_intention_formset-TOTAL_FORMS':u'5',
            'learning_intention_formset-INITIAL_FORMS':u'0',
        }
        response = self.client.post('/courses/1/lesson/1/edit/', mod_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lesson/lesson_edit.html')

    def test_lesson_edit_page_validation_errors_generate_error_msg(self):
        self.client.login(username='sven', password='sven')
        mod_data = {
            'lesson_form-code': '', 
            'lesson_form-name': '', 
            'lesson_form-abstract': '',
            'video_formset-0-url':'http://www.youtube.com/embed/E8HE',
            'video_formset-0-name':'',
            'video_formset-TOTAL_FORMS':u'1',
            'video_formset-INITIAL_FORMS':u'0',
            'attachment_formset-0-name':'',
            'attachment_formset-0-desc':'A failure',
            'attachment_formset-0-attachment':None,
            'attachment_formset-TOTAL_FORMS':u'1',
            'attachment_formset-INITIAL_FORMS':u'0',
            'learning_intention_formset-TOTAL_FORMS':u'5',
            'learning_intention_formset-INITIAL_FORMS':u'0',
        }
        response = self.client.post('/courses/1/lesson/1/edit/', mod_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(LESSON_NAME_FIELD_REQUIRED_ERROR, response.content)
        self.assertIn(LESSON_ABSTRACT_FIELD_REQUIRED_ERROR, response.content)
        self.assertIn(VIDEO_NAME_FIELD_REQUIRED_ERROR, response.content)
        self.assertIn(VIDEO_URL_FIELD_INVALID_ERROR, response.content)
        self.assertIn(ATTACHMENT_NAME_FIELD_REQUIRED_ERROR, response.content)
        self.assertIn(
            escape(ATTACHMENT_ATTACHMENT_FIELD_REQUIRED_ERROR), response.content)
 
    def test_lesson_edit_page_has_lesson_basics_area(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/1/lesson/1/edit/')
        self.assertIn('id_lesson_basics_area', response.content)
        self.assertIn('value="What is Blender for?"', response.content)
        self.assertIn(
            'Be clear what Blender is', response.content)

    def test_lesson_edit_page_has_video_area(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/1/lesson/1/edit/')
        self.assertIn('id_video_formset_area', response.content)

    def test_lesson_edit_page_has_attachment_area(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/1/lesson/1/edit/')
        self.assertIn('id_attachment_formset_area', response.content)

    def test_lesson_edit_page_has_learning_intention_area(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/courses/1/lesson/1/edit/')
        self.assertIn('id_learning_intention_formset_area', response.content)

    def test_lesson_edit_page_attachments_saved(self):
        self.client.login(username='sven', password='sven')
        fp = SimpleUploadedFile('atest.txt', 'A simple test file')
        mod_data = {
            'lesson_form-code': 'T1', 
            'lesson_form-name': 'Test Lesson', 
            'lesson_form-abstract': 'Not much',
            'video_formset-TOTAL_FORMS':u'0',
            'video_formset-INITIAL_FORMS':u'0',
            'attachment_formset-0-name':'Test',
            'attachment_formset-0-desc':'A test attach',
            'attachment_formset-0-attachment':fp,
            'attachment_formset-TOTAL_FORMS':u'1',
            'attachment_formset-INITIAL_FORMS':u'0',
            'learning_intention_formset-TOTAL_FORMS':u'5',
            'learning_intention_formset-INITIAL_FORMS':u'0',
        }
        response = self.client.post('/courses/1/lesson/1/edit/', mod_data)
        self.assertRedirects(response, '/courses/1/lesson/1/', 302, 200)
        response = self.client.get('/courses/1/lesson/1/')
        self.assertIn('A test attach', response.content)
        self.assertIn(
            '<a href=\'/interaction/attachment/1/download/\'>Test</a>', 
            response.content
        )

    def test_lesson_edit_page_learning_intentions_saved(self):
        self.client.login(username='sven', password='sven')
        fp = SimpleUploadedFile('atest.txt', 'A simple test file')
        mod_data = {
            'lesson_form-code': 'T1', 
            'lesson_form-name': 'Test Lesson', 
            'lesson_form-abstract': 'Not much',
            'video_formset-TOTAL_FORMS':u'0',
            'video_formset-INITIAL_FORMS':u'0',
            'attachment_formset-TOTAL_FORMS':u'1',
            'attachment_formset-INITIAL_FORMS':u'0',
            'learning_intention_formset-0-text':u'Speed',
            'learning_intention_formset-1-text':u'Acceleration',
            'learning_intention_formset-TOTAL_FORMS':u'5',
            'learning_intention_formset-INITIAL_FORMS':u'0',
        }
        response = self.client.post('/courses/1/lesson/1/edit/', mod_data)
        self.assertRedirects(response, '/courses/1/lesson/1/', 302, 200)
        response = self.client.get('/courses/1/lesson/1/')
        self.assertIn('Speed', response.content)
        self.assertIn('Acceleration', response.content)
