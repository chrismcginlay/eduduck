#outcome/tests/test_views.py
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseForbidden
from django.test import TestCase
from courses.models import Course
from lesson.models import Lesson
from profile.models import User, Profile 
from interaction.models import UserCourse
from ..models import LearningIntention, LearningIntentionDetail
from ..forms import LearningIntentionForm
from ..views import (
    _user_permitted_to_edit_course,
    SCInlineFormset,
    LOInlineFormset
)

class OutcomeViewTests_new(TestCase):
    """Newer tests for outcome views using fixtures"""

    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json',
        'outcome_lints.json',
        'interactions.json',
    ]
    
    def test__user_permitted_to_edit_course(self):
        self.client.login(username='sven', password='sven')
        course = Course.objects.get(pk=1)
        user = User.objects.get(username='sven') 
        self.assertTrue(_user_permitted_to_edit_course(user, course.id))

    def test_learning_intention_has_correct_context_vars_not_author(self):
        self.client.login(username='gaby', password='gaby5')
        lesson = Lesson.objects.get(pk=1)
        lint = LearningIntentionDetail.objects.get(pk=1)
        url1 = "/lesson/{0}/lint/{1}/".format(lesson.pk,lint.pk)
        response = self.client.get(url1)
        self.assertIn('progressSC', response.context,
            'Missing context var: progressSC')               
        self.assertIn('progressLO', response.context,
            'Missing context var: progressLO')               
        self.assertIn('usc_list', response.context,
            'Missing list of user interactions with SCs')
        self.assertIn('ulo_list', response.context,
            'Missing list of user interactions with LOs')
        ulo_list = response.context['ulo_list']
        usc_list = response.context['usc_list']
        self.assertEqual(type(lint), type(ulo_list[0][0]))
        self.assertEqual(type(lint), type(usc_list[0][0]))
        self.assertEqual(ulo_list[0][1], 'red')
        self.assertEqual(usc_list[0][1], 'red')
        self.assertEqual(ulo_list[0][2], None)
        self.assertEqual(usc_list[0][2], None)
        self.assertFalse(response.context['user_can_edit'])

    def test_learning_intention_has_correct_context_vars_is_author(self):
        self.client.login(username='sven', password='sven')
        lesson = Lesson.objects.get(pk=1)
        lint = LearningIntention.objects.get(pk=1)
        url1 = "/lesson/{0}/lint/{1}/".format(lesson.pk,lint.pk)
        response = self.client.get(url1)
        self.assertIsNone(response.context['progressSC'])               
        self.assertIsNone(response.context['progressLO'])               
        self.assertTrue(response.context['user_can_edit'])

    def test_learning_intention_has_edit_button_is_author(self):
        self.client.login(username='sven', password='sven')
        lesson = Lesson.objects.get(pk=1)
        lint = LearningIntention.objects.get(pk=1)
        url1 = "/lesson/{0}/lint/{1}/".format(lesson.pk,lint.pk)
        response = self.client.get(url1)
        self.assertContains(
            response, 
            "<a href='/lesson/1/lint/1/edit/' id='id_edit_lint'"\
            " class='pure-button pure-button-primary'>"\
            "Edit Learning Intention</a>",
            html=True
        )

    def test_learning_intention_has_no_edit_button_not_author(self):
        self.client.login(username='gaby', password='gaby5')
        lesson = Lesson.objects.get(pk=1)
        lint = LearningIntention.objects.get(pk=1)
        url1 = "/lesson/{0}/lint/{1}/".format(lesson.pk,lint.pk)
        response = self.client.get(url1)
        self.assertNotIn('id_edit_lint', response.content)

    #Tests for edit view function
    def test_edit_HttpForbidden_if_not_author(self):
        self.client.login(username='gaby', password='gaby5')
        url1 = "/lesson/1/lint/1/edit/"
        response = self.client.get(url1)
        self.assertIsInstance(response, HttpResponseForbidden)
        
    def test_edit_uses_correct_template_if_author(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/lesson/1/lint/1/edit/') 
        self.assertTemplateUsed(response, 'outcome/edit_lint.html')

    def test_edit_has_correct_context_vars_if_author(self):
        self.client.login(username='sven', password='sven')
        lesson = Lesson.objects.get(pk=1)
        lint = LearningIntentionDetail.objects.get(pk=1)
        url1 = "/lesson/{0}/lint/{1}/edit/".format(lesson.pk,lint.pk)
        response = self.client.get(url1)
        self.assertIn('li_form', response.context)
        self.assertIn('sc_formset', response.context)
        self.assertIn('lo_formset', response.context)
        self.assertIn('learning_intention', response.context)

    def test_edit_view_uses_correct_formsets_if_author(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/lesson/1/lint/1/edit/')
        self.assertIsInstance(
            response.context['li_form'], LearningIntentionForm)
        self.assertIsInstance(
            response.context['sc_formset'], SCInlineFormset)
        self.assertIsInstance(
            response.context['lo_formset'], LOInlineFormset)
        self.assertTrue(
            hasattr(response.context['sc_formset'], 'management_form'))
        self.assertTrue(
            hasattr(response.context['lo_formset'], 'management_form'))

    def test_edit_view_has_correct_page_title(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/lesson/1/lint/1/edit/')
        self.assertContains(
            response,
            "<h2 id='id_page_title'>Editing: "\
            "Recognise a range of tasks for w...",
            html=True
        )

    def test_edit_view_shows_breadcrumb(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/lesson/1/lint/1/edit/')
        self.assertIn(
            "<p id='id_breadcrumb'>",
            response.content
        ) 
        self.assertContains(
            response, 
            '<a href="/courses/">All Courses</a>',
            html=True
        )
        self.assertContains(
            response,
            '<a href="/courses/1/">Blender Home</a>',
            html=True
        )
        self.assertContains(
            response,
            '<a href="/courses/1/lesson/1/">Lesson Home</a>',
            html=True
        )
        self.assertContains(
            response,
            '<a href="/lesson/1/lint/1/">Learning Intention</a>',
            html=True
        )
        self.assertIn(
            '&gt; Edit',
            response.content
        )

    def test_edit_view_shows_existing_data_for_editing(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/lesson/1/lint/1/edit/')
        self.assertEqual(
            response.context['li_form']['text'].value(),
            u'Recognise a range of tasks for which Blender could be used'
        )
        self.assertEqual(
            response.context['sc_formset'][0]['text'].value(),
            u'Spot 3D modelling tasks'
        )
        self.assertEqual(
            response.context['sc_formset'][1]['text'].value(),
            u'Spot video sequencing tasks'
        )
        self.assertEqual(
            response.context['lo_formset'][0]['text'].value(),
            u'I can correctly identify or reject various tasks '\
            'as being well suited to Blender' 
        )
        self.assertEqual(
            response.context['lo_formset'][1]['text'].value(),
            u'I can state whether the main techique of a task involves '\
            'modelling, sequencing, animating or physics simulation'
        )

    def test_edit_view_form_shows_correct_error_messages(self):
        self.client.login(username='sven', password='sven')
        mod_data = {
            'learning_intention_form-text': '', #Should reject empty string
            'learning_intention_form-lesson': 1,
            'sc_formset-TOTAL_FORMS':u'6',
            'sc_formset-INITIAL_FORMS':u'0',
            'sc_formset-0-id':u'1', #prevent MultiVal dict key err.
            'sc_formset-0-text':'', #should reject empty string
            'lo_formset-TOTAL_FORMS':u'6',
            'lo_formset-INITIAL_FORMS':u'0',
            'lo_formset-0-id':u'2',
            'lo_formset-0-text':'', #should reject empty string
        }
        response = self.client.post('/lesson/1/lint/1/edit/', mod_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['li_form'].errors,
            {'text': [u'This field is required.']}
        )

    def test_edit_view_has_3_save_edits_buttons(self):
        self.client.login(username='sven', password='sven')
        response = self.client.get('/lesson/1/lint/1/edit/')
        self.assertContains(
            response, 
            "<button id='id_submit_lilosc_edits' "\
            "class='pure-button pure-button-primary' "\
            "type='submit'>Save All Edits</button>",
            html=True
        )
        self.assertContains(
            response, 
            "<button id='id_submit_lilosc_edits2' "\
            "class='pure-button pure-button-primary' "\
            "type='submit'>Save All Edits</button>",
            html=True
        )
        self.assertContains(
            response, 
            "<button id='id_submit_lilosc_edits3' "\
            "class='pure-button pure-button-primary' "\
            "type='submit'>Save All Edits</button>",
            html=True
        )

    def test_edit_view_edits_actually_saved_if_author(self):
        self.client.login(username='sven', password='sven')
        mod_data = {
            'learning_intention_form-text': 'Learn up some stuff', 
            'learning_intention_form-lesson': 1,
            'sc_formset-TOTAL_FORMS':u'6',
            'sc_formset-INITIAL_FORMS':u'0',
#            'sc_formset-0-id':u'1', #prevent multival dict key err.
            'sc_formset-0-text':'boo',
            'lo_formset-TOTAL_FORMS':u'6',
            'lo_formset-INITIAL_FORMS':u'0',
#            'lo_formset-0-id':u'2',
            'lo_formset-0-text':'Hoo',
        }
        ##This should trigger modification of the course
        response = self.client.post('/lesson/1/lint/1/edit/', mod_data)
        self.assertRedirects(response, '/lesson/1/lint/1/')
   
        ##Then visiting the course should reflect the changes
        response = self.client.get('/lesson/1/lint/1/')
        self.assertContains(response, 
            '<p>Learn up some stuff</p>', html=True)
        self.assertIn('boo', response.content)
        self.assertIn('Hoo', response.content)


class OutcomeViewTests(TestCase):
    """Test the outcome specific views"""
    
    course1_data = {'code': 'EDU02',
                   'name': 'A Course of Leeches',
                   'abstract': 'Learn practical benefits of leeches',
                   }
    lesson1_data = {
                    'name': 'Introduction to Music',
                    'abstract': 'A summary of what we cover',
                   }
                   
    def setUp(self):
        self.user1 = User.objects.create_user(
            'bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user('dave', 'dave@dave.com', 'dave')
        self.user2.is_active = True
        self.user2.save()
        self.course1 = Course(**self.course1_data)
        self.course1.instructor = self.user2
        self.course1.organiser = self.user2
        self.course1.save()
        self.lesson1 = Lesson(course=self.course1, **self.lesson1_data)
        self.lesson1.save()        
        self.learningintention1 = LearningIntention(
            lesson = self.lesson1, text = "Practise")
        self.learningintention1.save()                                            
        self.lid1 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            text = "Choose Topaz",
            lid_type = LearningIntentionDetail.SUCCESS_CRITERION
        )
        self.lid1.save()  
        self.lid2 = LearningIntentionDetail(
            learning_intention = self.learningintention1,
            text = "Eat fish",
            lid_type = LearningIntentionDetail.SUCCESS_CRITERION
        )                                        
        self.lid2.save()
        self.lid3 = LearningIntentionDetail(
            learning_intention = self.learningintention1, 
            text = "Calculate 6*9",
            lid_type = LearningIntentionDetail.LEARNING_OUTCOME
        )
        self.lid3.save()   
        
        self.profile1 = self.user1.profile
        self.profile1.accepted_terms = True
        self.profile1.signature_line = 'Learning stuff'
        self.profile1.save()
    
    def test_learning_intention(self):
        """Test view of a single learning intention"""
        
        les1 = self.lesson1.id
        lint1 = self.learningintention1.id
        url1 = "/lesson/{0}/lint/{1}/".format(les1,lint1)

        response = self.client.get(url1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(x in response.context
            for x in ['lesson_id', 'lesson_intention_id'])
        self.assertIn("Choose Topaz", response.content, "SC missing")
        self.assertIn("Calculate 6*9", response.content, "LO missing")

        cycle1 = "cycle{0}".format(self.lid1.id)
        cycle2 = "cycle{0}".format(self.lid2.id)
        self.assertIn(cycle1, response.content, "Cycle button missing")
        self.assertIn(cycle2, response.content, "Cycle button missing")

        #test non-existing LI        
        response = self.client.get('/lesson/1/lint/5000/')
        self.assertEqual(response.status_code, 404)
        
        #test not logged in
        response = self.client.get(url1)
        self.assertNotIn('progressSC', response.context)
        
        ### Success Criteria Cycle Tests
        #press some buttons and see what happens
        self.client.login(username='bertie', password='bertword')
        #Register user on course first:
        uc = UserCourse(course=self.course1, user=self.user1)
        uc.save() 

        #cycle to amber        
        response = self.client.post(url1, {cycle1:'Cycle'})
        self.assertEqual(response.status_code, 200)
        trafficlight = response.context['usc_list'][0][2].condition
        self.assertEqual(trafficlight, 1)
        self.assertInHTML(
            "<img id='id_SC1' class='tl-amber' "\
            "src='/static/images/img_trans.png'>",
            response.content)
        self.assertContains(
            response,
            '<li class="criterion" data-id="1">')
        self.assertIn(
            '<li class="learning_outcome" data-id="3">', 
            response.content)
        self.assertEqual(
            response.context['progressSC'], (0,2,2,100)) #progress bar
        self.assertEqual(
            response.context['progressLO'], (0,1,1,100)) #progress bar

        #cycle to green
        response = self.client.post(url1, {cycle1:'Cycle'})
        self.assertEqual(response.status_code, 200)
        trafficlight = response.context['usc_list'][0][2].condition
        self.assertEqual(trafficlight, 2)
        self.assertInHTML(
            "<img id='id_SC1' class='tl-green' "\
            "src='/static/images/img_trans.png'>",
            response.content)
        self.assertEqual(
            response.context['progressSC'], (1,1,2,100)) #progress bar
        self.assertEqual(
            response.context['progressLO'], (0,1,1,100)) #progress bar
    
        #cycle to red
        response = self.client.post(url1, {cycle1:'Cycle'})
        self.assertEqual(response.status_code, 200)
        trafficlight = response.context['usc_list'][0][2].condition
        self.assertEqual(trafficlight, 0)
        self.assertInHTML(
            "<img id='id_SC1' class='tl-red' "\
            "src='/static/images/img_trans.png'>",
            response.content)
        self.assertEqual(
            response.context['progressSC'], (0,2,2,100)) #progress bar
        self.assertEqual(
            response.context['progressLO'], (0,1,1,100)) #progress bar
