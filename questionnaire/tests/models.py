from django.test import TestCase
from django.db import models
from questionnaire.models import Question, QuestionGroup, Questionnaire, CustomListField, QuestionGroup_order, Question_order, CustomListField
from django.forms.fields import TextInput,CharField


class CustomListFieldTests(TestCase):
    fixtures = ['test_questionnaire_fixtures.json']
    def test_init(self):
        '''
            A new Custom List Field should have following attributes:
            1. Default=None
            2. Null=True
            3. blank=True
            4. help_text = non empty string (don't test the exact wording as this may change!)
            5. token=,
            
            and it should be a subclass of TextField
        '''
        string_test = 'A,B,C'
        new_custom_list = CustomListField(string_test)
        empty_string = ''
        
        self.assertEqual(new_custom_list.default, None)
        self.assertEqual(new_custom_list.null, True)
        self.assertEqual(new_custom_list.blank, True)
        self.assertEqual(new_custom_list.token, ',')
        self.assertNotEqual(new_custom_list.help_text, empty_string)
        self.assertTrue(isinstance(new_custom_list, models.TextField), 'CustomListField is an instance of TextField')
        


        
        
    def test_toPython_default(self):
        '''
           Given a string that is comma demlimited this should return you  a list of strings split by the comma
        '''
        string = 'A,B,C'
        expected_list = ['A', 'B', 'C']
        new_custom_list = CustomListField(string).to_python(string)
        self.assertEqual(new_custom_list, expected_list, 'The new custom list will return list as expected')
        self.assertEqual(type(new_custom_list), list, 'The string with delimiter returns object type list')
        
        
        
        
    def test_toPython_customized(self):
        '''
           If a token is specified e.g. | then a string that is delimited with this is returned a s a list split by it
        '''
        self.assert_(False, 'Not yet implemented')
        
    def test_toPython_empy_null_string(self):
        '''
           if the value is empty or None, should return an empty list, not an error.
        '''
        string = ''
        #expected_list = []
        new_custom_list = CustomListField(string).to_python(string)
        #self.assertEqual(new_custom_list, expected_list, 'The new custom list will return empty list as expected')
        self.assertEqual(new_custom_list, None, 'Empty list will return None, instead of Error')

        
    def test_db_prep_value_default(self):
        '''
            Should return a string delimited by a comma based on the value passed in 
        '''
        string = 'A,B,C'
        expected_list = ['A', 'B', 'C']
        new_custom_list = CustomListField(string)

        get_db_prep_value = new_custom_list.get_db_prep_value(expected_list, expected_list)
        self.assertEqual(get_db_prep_value, string)
        
    
    def test_db_prep_value_custom(self):
        '''
            Should return a string delimited by whatever was specified as the token based on the value passed in 
        '''
        self.assert_(False, 'Not yet implemented')
    
    def test_value_to_string(self):
        '''
            assuming the object passed in is a CustomListField poulated with a value
            this should do the same as test_db_prep_value_default
        '''
        string = 'A,B,C'
        expected_list = ['A', 'B', 'C']
        new_custom_list = CustomListField(string)
        value_to_string = new_custom_list.value_to_string(new_custom_list)
        print value_to_string
        
class QuestionTestCase(TestCase):
    fixtures = ['test_questionnaire_fixtures.json']
    
    def test_all_fields(self):
        '''
            A Question object should define:
            1.Label which is a Charfield, max_length = 100
            2.field_type whcih is a charfield with choices:
                a. charfield
                b. textfield
                c. booleanfield
                d. select_dropdown_field
                e. radioselectfield
                f. multiplechoicefield
            3. selectoptions which is a CustomListField
        '''
        

        
        question_label101 = Question.objects.create(label='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 
                                                   field_type='charfield', selectoptions=None)
        self.assertIsInstance(question_label101, CharField)
        self.assertLessEqual(len(question_label101.label), 100,'label length is greater than 100')
        self.assertEqual(question_label101.field_type, 'charfield', 'field_type is not charfield')
        self.assertIsInstance(question_label101.field_type, CustomListField, 'field_type is not an instance of CustomListField')
        
        question_textfield = Question.objects.create(label='question_textfield', field_type='charfield', selectoptions=None)
        self.assertEqual(question_textfield.field_type, 'textfield', 'field_type is not textfield')
        
        question_booleanfield = Question.objects.create(label='question_booleanfield', field_type='charfield', selectoptions=None)
        self.assertEqual(question_booleanfield.field_type, 'boolean', 'field_type is not booleanfield')
        
        question_select_dropdown_field = Question.objects.create(label='question_select_dropdown_field', field_type='select_dropdown_field', selectoptions=None)
        self.assertEqual(question_select_dropdown_field.field_type, 'select_dropdown_field', 'field_type is not select_dropdown_field')
        
        question_radioselectfield = Question.objects.create(label='question_radioselectfield', field_type='radioselectfield', selectoptions=None)
        self.assertEqual(question_radioselectfield.field_type, 'radioselectfield', 'field_type is not radioselectfield')
        
        question_multiplechoicefield = Question.objects.create(label='question_multiplechoicefield', field_type='multiplechoicefield', selectoptions=None)
        self.assertEqual(question_multiplechoicefield.field_type, 'multiplechoicefield', 'field_type is not multiplechoicefield')
        
    def test_required_fields(self):
        '''
            label and field_type are mandatory, you should not be able to save without these fields
            you should be able to save without selectoptions
        '''
        question_test = Question.objects.create(label='question_test', field_type=None, selectoptions=None)
        question_test1 = Question.objects.create(label='question_test1', field_type='charfield', selectoptions=None)
        
        self.assertFalse(question_test.save(),"can't be saved without field_type")
        self.assertTrue(question_test1.save(), 'can be saved')
         
    def test_save(self):
        '''
            If the field type is not either select_dropdown_field, radioselectfield or multiplechoicefield
            then the selectoptions should be set as None prior to saving (even if select options have been set)
        '''
        question_test1 = Question.objects.create(label='question_test1', field_type='textfield', selectoptions='Select 1,Select 2,Select 3')
        question_test2 = Question.objects.create(label='question_test2', field_type='charfield', selectoptions='Select 1,Select 2,Select 3')
        question_test3 = Question.objects.create(label='question_test3', field_type='boolean', selectoptions='Select 1,Select 2,Select 3')
        question_test4 = Question.objects.create(label='question_test4', field_type='select_dropdown_field', selectoptions='Select 1,Select 2,Select 3')
        question_test5 = Question.objects.create(label='question_test5', field_type='radioselectfield', selectoptions='Select 1,Select 2,Select 3')
        question_test6 = Question.objects.create(label='question_test6', field_type='multiplechoicefield', selectoptions='Select 1,Select 2,Select 3')
        question_test1.save()
        question_test2.save()
        question_test3.save()
        question_test4.save()
        question_test5.save()
        question_test6.save()
        self.assertEqual(question_test1.selectoptions, None, 'question_test1.selectoption is not None')
        self.assertEqual(question_test2.selectoptions, None, 'question_test2.selectoption is not None')
        self.assertEqual(question_test3.selectoptions, None, 'question_test3.selectoption is not None')
        self.assertNotEqual(question_test4.selectoptions, None, 'question_test4.selectoption is None')
        self.assertNotEqual(question_test5.selectoptions, None, 'question_test5.selectoption is None')
        self.assertNotEqual(question_test6.selectoptions, None, 'question_test6.selectoption is None')
        
        
class QuestionGroupTestCase(TestCase):
    fixtures = ['test_questionnaire_fixtures_formodels.json']
    
    def test_fields_all_fields(self):
        '''
            A QuestionGroup must have :
            1. name - which is a charfield, has a max length of 255 and should be unique and *required*
            2. questions ManyToMay field related to Question through question_order
        '''
        question_group_test = QuestionGroup.objects.get(pk=1)
        self.assertIsInstance(question_group_test.name, models.CharField, 'question_group_test.name is not an instance of models.CharField')
        self.assertLessEqual(len(question_group_test.name), 255, 'name length is %s, greater than 255' %(len(question_group_test.name)))
        
        
    def test_required_fields(self):
        '''
            Name is required so you should not be able to save the object without it
        '''
        question_group_test1 = QuestionGroup.objects.create()
        self.assertFalse(question_group_test1.save())
          
    def test_get_ordered_questions(self):
        '''
            This function should give you a list of Question objects, this list should be based upon the order_info
            provided by the through relationship with Question_order
        '''
        question_group_test = QuestionGroup.objects.get(pk=1)
        questions = question_group_test.get_ordered_questions()
        question_order1 = Question_order.objects.get(pk=1)
        question_order2 = Question_order.objects.get(pk=2)
        question_order3 = Question_order.objects.get(pk=3) 
        self.assertEqual(questions[0].label, question_order1.question.label)
        self.assertEqual(questions[1].label, question_order2.question.label)
        self.assertEqual(questions[2].label, question_order3.question.label)
       
class QuestionnaireTestCase(TestCase):
    fixtures = ['test_questionnaire_fixtures_formodels.json']
    
    def test_fields_all_fields(self):
        '''
            A Questionaire must have :
            1. name - which is a charfield, has a max length of 255 and should be unique and *required*
            2. questiongroups ManyToMay field related to QuestionGroup through questionGroup_order
        '''
        questionnaire_test = Questionnaire.objects.get(pk=2)
        self.assertIsInstance(questionnaire_test.name, models.CharField, 'question_group_test.name is not an instance of models.CharField')
        self.assertLessEqual(len(questionnaire_test.name), 250, 'name length is %s, greater than 255' %(len(questionnaire_test.name)))
        
    def test_required_fields(self):
        '''
            Name is required so you should not be able to save the object without it
        '''
        questionnaire_test1 = Questionnaire.objects.create()
        self.assertFalse(questionnaire_test1.save())
        
    def test_get_ordered_question_group(self):
        '''
            This function should give you a list of QuestionGroup objects, this list should be based upon the order_info
            provided by the through relationship with QuestionGroup_order
        '''
        questionnaire_test = Questionnaire.objects.get(pk=1)
        question_group = questionnaire_test.get_ordered_groups()
        question_group1 = QuestionGroup_order.objects.get(pk=1)
        question_group2 = QuestionGroup_order.objects.get(pk=2) 
        self.assertEqual(question_group[0].questiongroup.name, question_group1.questiongroup.name)
        self.assertEqual(question_group[1].questiongroup.name, question_group2.questiongroup.name)
        
class Questiongroup_OrderTestCase(TestCase):
    
    def test_fields(self):
        '''
            QuestionGroup_order should have the following fields (all of which are required):
            questiongroup = ForeignKey relationship with QuestionGroup
            questionnaire = ForeignKey relationship with Questionnaire
            order_info = IntegerField
        '''
        self.assert_(False, 'Not yet implemented')
        
    def test_required_fields(self):
        '''
            You shouldn't be able to make a QuestionGroup_order without any of the fields
        '''
        QuestionGroup_order_test = QuestionGroup_order.objects.create()
        self.assertFalse(QuestionGroup_order_test.save())
        
    
        
class Question_OrderTestCase(TestCase):
    
    def test_fields(self):
        '''
            Question_order should have the following fields (all of which are required):
            question = ForeignKey relationship with Question
            questionnaire = ForeignKey relationship with Questionnaire
            order_info = IntegerField
        '''
        self.assert_(False, 'Not yet implemented')
        
    def test_required_fields(self):
        '''
            You shouldn't be able to make a QuestionGroup_order without any of the fields
        '''
        Question_order_test = QuestionGroup_order.objects.create()
        self.assertFalse(Question_order_test.save())
        
    
        
class AnswerSetTestCase(TestCase):
    
    def test_fields(self):
        '''
            An AnswerSet should have the following required fields:
            1. User - FK to django.auth.models.User
            2. questionniare - FK to Questionnaire
        '''
        self.assert_(False, 'Not yet implemented')
        
    def test_required_fields(self):
        '''
            An AnswerSet should not be able to be saved without all of its fields present
        '''
        self.assert_(False, 'Not yet implemented')
        
    
class QuestionAnswerTestCase(TestCase):
    
    def test_fields(self):
        '''
            A Question Answer should ahve the following fields:
            1. question - FK to a Question
            2. answer - Charfield max length = 255 can be blank
            3. answer_Set - FK to a AnswerSet object
        '''
        self.assert_(False, 'Not yet implemented')
        
    def test_required_fields(self):
        '''
            You shouldn't be able to save a QuestionAnswer without question or answer_Set
            However you should be able to do without specifying an answer, and this should be saved as an empty string.
        '''
        
        
