#courses/tests/test_views.py

import json
import os
from datetime import datetime
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http.response import HttpResponseForbidden
from django.test import TestCase
from django.utils.html import escape

from profile.models import Profile
from interaction.models import (
    UserAttachment,
    UserCourse,
    UserLesson,
)
from attachment.models import Attachment
from attachment.forms import (
    ATTACHMENT_NAME_FIELD_REQUIRED_ERROR,
    ATTACHMENT_ATTACHMENT_FIELD_REQUIRED_ERROR,
)
from checkout.models import PricedItem 
from lesson.forms import LESSON_NAME_FIELD_REQUIRED_ERROR
from lesson.models import Lesson
from video.utils import VIDEO_URL_FIELD_INVALID_ERROR
from ..forms import (
    COURSE_NAME_FIELD_REQUIRED_ERROR,
    COURSE_ABSTRACT_FIELD_REQUIRED_ERROR,
    )
from ..models import Course
from ..views import (
    CourseFullForm,
    _courses_n_24ths,
    _user_permitted_to_edit_course,
    _user_permitted_to_publish_course,
    LessonInlineFormset,
    VideoInlineFormset,
    AttachmentInlineFormset
    )

class CourseViewTests(TestCase):
    """Test the course views"""
    
    course1_data = {
        'code': 'EDU02',
        'name': 'A Course of Leeches',
        'abstract': 'Learn practical benefits of leeches',
        'published': True,
    }
    course2_data = {
        'code': 'FBR9',
        'name': 'Basic Knitting',
        'abstract': 'Casting on',
    'published': True,
    }  
    course3_data = {
        'code': 'G3',
        'name': 'Nut Bagging',
        'abstract': 'Put the nuts in the bag',
        'published': True,
    }
    course4_data = {
        'code': 'W1',
        'name': 'Washing',
        'abstract': 'How to *wash* a cat',
        'published': True,
    }
    course5_data = {
        'code': 'E1',
        'name': 'Electronics',
        'abstract': 'Intro to Electronics',
        'published': False,
    }
    lesson1_data = {
        'name': 'Introduction to Music',
        'abstract': 'A summary of what we cover',
    }
    lesson2_data = {
        'name': 'Stuff',
        'abstract': 'Not a lot',
    }

    def setUp(self):
        self.user1 = User.objects.create_user(
            'bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user(
            'hank', 'hank@example.com', 'hankdo')
        self.user2.is_active = True
        self.user2.save()

        self.course1 = Course(**self.course1_data)
        self.course1.organiser = self.user1
        self.course1.instructor = self.user1
        self.course1.save()

        self.course2 = Course(**self.course2_data)
        self.course2.organiser = self.user1
        self.course2.instructor = self.user2
        self.course2.save()

        self.course3 = Course(**self.course3_data)
        self.course3.organiser = self.user2
        self.course3.instructor = self.user2
        self.course3.save()
        
        self.course4 = Course(**self.course4_data)
        self.course4.organiser = self.user2
        self.course4.instructor = self.user2
        self.course4.save()

        self.course5 = Course(**self.course5_data)
        self.course5.organiser = self.user2
        self.course5.instructor = self.user2
        self.course5.save()

        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()
        self.lesson2 = Lesson(course=self.course3, **self.lesson2_data)
        self.lesson2.save()
        
    def tearDown(self):
        testfile = os.getcwd()+'/media/attachments/atest.txt'
        if os.path.isfile(testfile):
            os.remove(testfile)

    def test__user_permitted_to_edit_course(self):
        self.client.login(username='bertie', password='bertword')
        course = Course.objects.get(pk=1)
        user = User.objects.get(username='bertie') 
        self.assertTrue(_user_permitted_to_edit_course(user, course.id))

    def test__user_permitted_to_publish_course(self):
        self.client.login(username='hank', password='hankdo')
        course = Course.objects.get(pk=1)
        user = User.objects.get(username='hank') 
        self.assertFalse(_user_permitted_to_publish_course(user, course.id))
        self.client.logout()

        self.client.login(username='bertie', password='bertword')
        course = Course.objects.get(pk=1)
        user = User.objects.get(username='bertie') 
        self.assertTrue(_user_permitted_to_publish_course(user, course.id))

    def test_helper__courses_n_24ths_returns_list(self):
        course_list = Course.objects.all()
        cn24 = _courses_n_24ths(course_list)
        self.assertIsInstance(cn24, list)
        self.assertIs(type(cn24[0]), tuple)    #entry should be 2-tuple
        self.assertEqual(len(course_list), len(cn24))        
        
    def test_course_page_has_no_enrol_button_for_organiser_instructor(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/')
        self.assertNotIn("id='id_enrol_button'", response.content)
        self.assertNotIn("id='id_enrol_button2'", response.content)

    def test_course_page_has_edit_button_for_organiser_instructor(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/')
        self.assertContains(
        response, 
        "<a href='/courses/1/edit/' id='id_edit_course' class='pure-button pure-button-primary'>Edit Course</a>",
        html=True)
        self.assertEqual(response.context['user_can_edit'], True)

    def test_course_page_has_no_edit_button_if_not_organiser_instructor(self):
        self.client.login(username='hank', password='hankdo')
        response = self.client.get('/courses/1/')
        self.assertNotIn("id='id_edit_course'", response.content)
        self.assertEqual(response.context['user_can_edit'], False)

    def test_course_edits_actually_saved(self):
        self.client.login(username='bertie', password='bertword')
        fp = SimpleUploadedFile('atest.txt', 'A simple test file')
        mod_data = {
            'course_form-code': 'F1', 
            'course_form-name': 'Dingbat', 
            'course_form-abstract': 'Fingbot',
            'course_form-organiser': self.user1,
            'course_form-instructor': self.user1,
            'lesson_formset-TOTAL_FORMS':4,
            'lesson_formset-INITIAL_FORMS':1,
            'lesson_formset-0-id':u'1', #prevent MultiVal dict key err.
            'lesson_formset-0-name':'Boo',
            'lesson_formset-0-abstract':'Hoo',
            'video_formset-0-url':'http://www.youtube.com/embed/EJiUWBiM8HE',
            'video_formset-0-name':'Cmdr Hadfield\'s Soda',
            'video_formset-TOTAL_FORMS':u'1',
            'video_formset-INITIAL_FORMS':u'0',
            'attachment_formset-0-name':'A test file',
            'attachment_formset-0-desc':'A description of a file',
            'attachment_formset-0-attachment':fp,
            'attachment_formset-TOTAL_FORMS':u'1',
            'attachment_formset-INITIAL_FORMS':u'0'
        }
        ##This should trigger modification of the course
        response = self.client.post('/courses/1/edit/', mod_data)
        self.assertRedirects(response, '/courses/1/')

        ##Then visiting the course should reflect the changes
        response = self.client.get('/courses/1/')
        self.assertContains(response, 
            '<h3>F1 : Dingbat Course Homepage</h3>', html=True)
        self.assertContains(response, '<p>Fingbot</p>', html=True)
        self.assertIn('Boo</a>', response.content)
        self.assertIn('<p>Hoo', response.content)
        self.assertIn(escape('Cmdr Hadfield\'s Soda'), response.content)
        self.assertIn('EJiUWBiM8HE', response.content) #youtube video
        self.assertIn('A test file', response.content)
        self.assertIn('A description of a file', response.content)
        target = "<a href='/interaction/attachment/1/download/'>A test file</a>"
        self.assertIn(target, response.content)

    def test_course_edit_redirects_if_not_loggedin(self):
        response = self.client.get('/courses/1/edit/')  
        login_redirect_url = '/accounts/login/?next=/courses/1/edit/'
        self.assertRedirects(response, login_redirect_url, 302, 200)

    def test_course_edit_forbidden_if_user_not_permitted(self):
        self.client.login(username='hank', password='hankdo')
        response = self.client.get('/courses/1/edit/')
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_course_edit_200_if_user_permitted(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/') 
        self.assertEqual(response.status_code, 200)

    def test_course_edit_page_has_correct_title_and_breadcrumb(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/')
        needle = "<h2 id='id_page_title'>Editing: A Course of Leeches</h2>"
        self.assertIn(needle, response.content)
        self.assertIn("<p id='id_breadcrumb'>", response.content)
        self.assertContains(
            response, 
            '<a href="/courses/">All Courses</a>',
            html=True)
        self.assertContains(
            response, 
            '<a href="/courses/1/">A Course of Leeches</a>',
            html=True)

    def test_course_edit_uses_correct_template(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/') 
        self.assertTemplateUsed(response, 'courses/course_edit.html')
        
    def test_course_edit_page_uses_correct_form(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/')
        self.assertIsInstance(response.context['course_form'], CourseFullForm)
        
    def test_course_edit_page_uses_correct_formsets(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/')
        self.assertIsInstance(
            response.context['lesson_formset'], LessonInlineFormset)
        self.assertIsInstance(
            response.context['video_formset'], VideoInlineFormset)
        self.assertIsInstance(
            response.context['attachment_formset'], AttachmentInlineFormset)
        self.assertTrue(
            hasattr(response.context['lesson_formset'], 'management_form'))
        self.assertTrue(
            hasattr(response.context['video_formset'], 'management_form'))
        self.assertTrue(
            hasattr(response.context['attachment_formset'], 'management_form'))


    def test_course_edit_page_validation_errors_sent_to_template(self):
        self.client.login(username='bertie', password='bertword')
        data = {
            'course_form-code': '',
            'course_form-name': '',
            'course_form-abstract': '',
            'lesson_formset-0-id':u'1', #prevent MultiVal dict key err.
            'lesson_formset-TOTAL_FORMS':u'4',
            'lesson_formset-INITIAL_FORMS':u'1',
            'video_formset-0-url':'err://err.err/EJiUWBiM8HE',
            'video_formset-TOTAL_FORMS':u'1',
            'video_formset-INITIAL_FORMS':u'0',
            'attachment_formset-TOTAL_FORMS':u'1',
            'attachment_formset-INITIAL_FORMS':u'0'
        }
        response = self.client.post('/courses/1/edit/', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_edit.html')
       
    def test_course_edit_page_validation_errors_generate_error_msg(self):
        self.client.login(username='bertie', password='bertword')
        ##First with missing basic course data
        data = {
            'course_form-code': '',
            'course_form-name': '',
            'course_form-abstract': '',
            'lesson_formset-0-id':u'1', #prevent MultiVal dict key err.
            'lesson_formset-TOTAL_FORMS':u'4',
            'lesson_formset-INITIAL_FORMS':u'1',
            'video_formset-0-url':'http://youtu.be/EJiUWBiM8HE',
            'video_formset-TOTAL_FORMS':u'1',
            'video_formset-INITIAL_FORMS':u'0',
            'attachment_formset-TOTAL_FORMS':u'1',
            'attachment_formset-INITIAL_FORMS':u'0'
        }
        response = self.client.post('/courses/1/edit/', data)
        self.assertIn('Please correct the following:', response.content)
        self.assertIn(COURSE_NAME_FIELD_REQUIRED_ERROR, response.content)
        self.assertIn(COURSE_ABSTRACT_FIELD_REQUIRED_ERROR, response.content)

        ##Then with missing required fields in lesson formset
        data = {
            'course_form-code': 'T1',
            'course_form-name': 'Test',
            'course_form-abstract': 'With some invalid lessons',
            'lesson_formset-0-id':u'1', #prevent MultiVal dict key err.
            'lesson_formset-0-name':'',
            'lesson_formset-TOTAL_FORMS':u'4',
            'lesson_formset-INITIAL_FORMS':u'1',
            'video_formset-0-url':'http://youtu.be/EJiUWBiM8HE',
            'video_formset-TOTAL_FORMS':u'1',
            'video_formset-INITIAL_FORMS':u'0',
            'attachment_formset-TOTAL_FORMS':u'1',
            'attachment_formset-INITIAL_FORMS':u'0'
        }
        response = self.client.post('/courses/1/edit/', data)
        self.assertIn('Please correct the following:', response.content)
        self.assertIn(LESSON_NAME_FIELD_REQUIRED_ERROR, response.content)

        ##And with invalid url in video formset
        data = {
            'course_form-code': 'T1',
            'course_form-name': 'Test',
            'course_form-abstract': 'With invalid video url',
            'lesson_formset-0-id':u'1', #prevent MultiVal dict key err.
            'lesson_formset-0-name':'Test',
            'lesson_formset-TOTAL_FORMS':u'4',
            'lesson_formset-INITIAL_FORMS':u'1',
            'video_formset-0-id':u'1', #prevent MultiVal dict key err.
            'video_formset-0-name':'Invalid url',
            'video_formset-0-url':'htp://yotub.vom/56tyY',
            'video_formset-TOTAL_FORMS':u'1',
            'video_formset-INITIAL_FORMS':u'0',
            'attachment_formset-TOTAL_FORMS':u'1',
            'attachment_formset-INITIAL_FORMS':u'0'
        }
        response = self.client.post('/courses/1/edit/', data)
        self.assertIn('Please correct the following:', response.content)
        self.assertIn(VIDEO_URL_FIELD_INVALID_ERROR, response.content)	
        
        ## Then with missing attachment data
        data = {
            'course_form-code': 'T1',
            'course_form-name': 'Test',
            'course_form-abstract': 'With invalid video url',
            'lesson_formset-0-id':u'1', #prevent MultiVal dict key err.
            'lesson_formset-0-name':'Test',
            'lesson_formset-TOTAL_FORMS':u'4',
            'lesson_formset-INITIAL_FORMS':u'1',
            'video_formset-TOTAL_FORMS':u'1',
            'video_formset-INITIAL_FORMS':u'0',
            'attachment_formset-0-id':u'1',
            'attachment_formset-0-name':'',
            'attachment_formset-0-attachment':None,
            'attachment_formset-0-desc':'A failure',
            'attachment_formset-TOTAL_FORMS':u'1',
            'attachment_formset-INITIAL_FORMS':u'0'
        }
        response = self.client.post('/courses/1/edit/', data)
        self.assertIn('Please correct the following:', response.content)
        self.assertIn(ATTACHMENT_NAME_FIELD_REQUIRED_ERROR, response.content)	
        self.assertIn(
            escape(ATTACHMENT_ATTACHMENT_FIELD_REQUIRED_ERROR), 
            response.content
        )
       
    def test_course_edit_page_has_course_detail_area(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/')
        self.assertIn('id_course_basics_area', response.content)
        self.assertIn('value="EDU02"', response.content)
        self.assertIn('value="A Course of Leeches"', response.content)
        self.assertIn(
            'Learn practical benefits of leeches', response.content)

    def test_course_edit_page_has_populated_lesson_area(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/')
        self.assertIn('id_lesson_formset_area', response.content)
        self.assertIn('Introduction to Music', response.content)

    def test_course_edit_page_has_video_area(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/')
        self.assertIn('id_video_formset_area', response.content)

    def test_course_edit_page_has_attachment_area(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/')
        self.assertIn('id_attachment_formset_area', response.content)

    def test_course_edit_attachment_area_doesnt_show_lesson_fk(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/edit/')
        self.assertNotRegexpMatches(
            response.content, 
            'id_attachment_formset-\d+-lesson',
            'Lesson field shouldn\'t be showing up')

    def test_course_create_redirects_if_not_loggedin(self):
        response = self.client.get('/courses/create/')
        login_redirect_url = '/accounts/login/?next=/courses/create/'
        self.assertRedirects(response, login_redirect_url, 302, 200)
        
    def test_course_create_page_200_if_loggedin(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        self.assertEqual(response.status_code, 200)

    def test_course_create_view_uses_correct_template(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        self.assertTemplateUsed(response, 'courses/course_create.html')
        
    def test_course_create_view_uses_correct_form(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        self.assertIsInstance(response.context['form'], CourseFullForm)
        
    def test_course_create_page_has_correct_title_and_breadcrumb(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        needle = "<h2 id='id_page_title'>Create a Course</h2>"
        self.assertIn("<p id='id_breadcrumb'>", response.content)
        self.assertIn(needle, response.content)
        
    def test_course_create_page_has_correct_fields(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        self.assertIn('<input id="id_code"', response.content)
        self.assertIn('<input id="id_name"', response.content)
        self.assertIn('id="id_abstract"', response.content)

    def test_course_create_page_has_create_button(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        target = 'id="id_course_create"'
        self.assertIn(target, response.content)
        
    def test_course_create_page_invalid_form_sent_to_template(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.post('/courses/create/', data={
            'code': '',
            'name': '',
            'abstract': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_create.html')
            
    def test_course_create_page_validation_errors_sent_to_template(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.post('/courses/create/', data={
            'code': '',
            'name': '',
            'abstract': '',
        })
        expected_errors = (
            COURSE_NAME_FIELD_REQUIRED_ERROR,
            COURSE_ABSTRACT_FIELD_REQUIRED_ERROR,
        )
        for err in expected_errors:
            self.assertContains(response, err)

    def test_course_create_page_doesnot_show_errors_by_default(self):
        """ Check that errors don't show up when the form first loads """
        
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/create/')
        not_expected_errors = (
            COURSE_NAME_FIELD_REQUIRED_ERROR,
            COURSE_ABSTRACT_FIELD_REQUIRED_ERROR,
            )
        for err in not_expected_errors:
            self.assertNotContains(response, err)
            
        
    def test_course_create_page_invalid_form_passes_form_to_template(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.post('/courses/create/', data={
            'code': '',
            'name': '',
            'abstract': ''
        })
        self.assertIsInstance(response.context['form'], CourseFullForm)

    def test_course_create_page_can_save_data(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.post('/courses/create/', data={
            'code': 'T01',
            'name': 'Test',
            'abstract': 'A test course'
        })
        self.assertRedirects(response, '/courses/6/', 302, 200)
        response = self.client.get('/courses/6/')
        self.assertIn('T01', response.content)
        self.assertIn('Test', response.content)
        self.assertIn('A test course', response.content)
         
    def test_course_enrol_page_requires_login(self):
        response = self.client.get('/courses/1/enrol/')
        login_redirect_url = '/accounts/login/?next=/courses/1/enrol/'
        self.assertRedirects(response, login_redirect_url, 302, 200)

    def test_course_enrol_page_200_if_loggedin(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/enrol/')
        self.assertEqual(response.status_code, 200)

    def test_course_enrol_page_uses_correct_template(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/enrol/')
        self.assertTemplateUsed(response, 'courses/course_enrol.html')

    def test_course_enrol_page_has_enrol_button(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/3/enrol/')
        target = "id='id_enrol_button'"
        self.assertIn(target, response.content)

    def test_course_enrol_page_no_enrol_button_if_author(self):
        """Course organiser or instructor can't enrol!"""
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/enrol/')
        target1 = "id='id_enrol_button'"
        self.assertNotIn(target1, response.content)
        target2 = "you can't enrol since you are involved in running "\
            "this course."
        self.assertIn(target2, response.content)

    def test_course_enrol_page_has_correct_context_vars(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/1/enrol/')
        self.assertIn('course', response.context)
        self.assertIn('status', response.context)
        self.assertIn('fee_value', response.context)

    def test_course_enrol_page_status_auth_enrolled(self):
        """An authenticated and enrolled user status is passed to template"""

        self.client.login(username='bertie', password='bertword')
        #Enrol the user on the course (bertie is not organiser)
        uc = UserCourse(user=self.user1, course=self.course3)
        uc.save()
        response = self.client.get('/courses/3/enrol/')
        self.assertEqual('auth_enrolled', response.context['status'],
            "Registration status should be auth_enrolled")

    def test_course_enrol_page_status_noenrol(self):
        """Course instructor/organiser bar_enrol status passed to template"""
        self.client.login(username='bertie', password='bertword')
        #bert is course organiser
        response = self.client.get('/courses/1/enrol/')
        self.assertEqual('auth_bar_enrol', response.context['status'],
            "Registration status should be auth_bar_enrol")

    def test_enrol_page_abstract_renders_markdown(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/4/enrol/')
        self.assertIn('How to <em>wash</em> a cat', response.content)

    def test_enrol_page_has_organiser_instructor_links(self):
        """Course enrol template has correct links to instructor etc"""

        self.client.login(username='bertie', password='bertword')
        # Load up a course enrol page
        c2 = self.course2
        c2.instructor.first_name="Hank"
        c2.instructor.last_name="Rancho"
        c2.instructor.save()
        url2 = '/courses/{0}/enrol/'.format(c2.pk)
        response = self.client.get(url2)

        # Check username appears for organiser
        org = c2.organiser
        t = '<p>Course organiser <a href="/accounts/profile/{1}/public/">{0}</a>'
        target = t.format(org.username, org.pk)
        resp = response.content.replace("\n", "").replace("\t", "")
        self.assertIn(target, resp)
        
        # Check full name appears for instructor
        inst = c2.instructor
        t = '<p>Course instructor <a href="/accounts/profile/{1}/public/">{0}</a>'
        target = t.format(inst.get_full_name(), inst.pk)
        self.assertIn(target, resp)

    def test_course_enrol_page_shows_free_course_enrol(self):
        """Free courses allow direct enrolment, no payment overlay"""
        
        self.client.login(username='bertie', password='bertword')
        course5 = Course.objects.get(pk=5)
        priced_item = PricedItem.objects.get(object_id=course5.id)
        priced_item.fee_value = 0
        priced_item.save()
        response = self.client.get('/courses/5/enrol/')
        self.assertEqual(response.context['fee_value'], priced_item.fee_value)
        self.assertEqual(priced_item.fee_value, 0)  #testing a free course
        self.assertRegexpMatches(
            response.content,
            "<button id=\\\'id_enrol_button\\\'[\s\S]*Enrol &#163;Free"\
            "[\S\s]*<\/button>")

    def test_course_enrol_stripe_Pay_with_Card_not_visible_free_course(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/courses/5/enrol')   #free course
        self.assertNotIn('stripe-button', response.content)

    def test_course_index_not_logged_in(self):
        """Check course index page loads OK and has correct variables"""

        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
        #Next check template variables are present
        self.assertTrue(
            x in response.context for x in ['course_list', 'course_count'])

    def test_course_index_logged_in(self):
        """Check course index loads for logged in user"""

        url1 = '/courses/'
        self.client.login(username='bertie', password='bertword')
        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)
        self.assertIn('course_list', response.context, \
            "Missing template var: course_list")
        self.assertIn('course_count', response.context, \
            "Missing template var: course_count")
        
    def test_course_index_only_shows_published_courses(self):
        response = self.client.get('/courses/')
        self.assertIn('A Course of Leeches', response.content)
        self.assertIn('Basic Knitting', response.content)
        self.assertIn('Nut Bagging', response.content)
        self.assertIn('Washing', response.content)
        self.assertNotIn('Electronics', response.content)

    def test_course_index_shows_unpublished_course_to_author(self):
        self.client.login(username='hank', password='hankdo')
        response = self.client.get('/courses/')
        self.assertIn('A Course of Leeches', response.content)
        self.assertIn('Basic Knitting', response.content)
        self.assertIn('Nut Bagging', response.content)
        self.assertIn('Washing', response.content)
        self.assertIn('Electronics', response.content)
