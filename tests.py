#UNIT TEST FOR SURVEY CREATION
from surveyF import *
from mvc import *
import unittest
#Create a new class that inherits from TestCase
class TestCreation(unittest.TestCase):
#Define initialisation tasks that are executed before the tests are run
    def setUp(self):
        self.course = "COMP9999 17s2"
        self.course2 = "COMP1521 17s2"
        self.semester = "17s2"
        self.question = "Hello what is your name"
        self.falseQuestion = "This question does not exist in the list"
        self.type = "TEXT"
        self.user = "1111111111"
        self.realUser = "100"
        self.questionNumber = 1
        self.answer = "My name is John Doe"
        self.start_date = "22/10/17"
        self.start_time = "15:00"
        self.end_date = "30/11/17"
        self.end_time = "15:00"
     
    #Define the test-cases
    def test_survey_creation_success(self):
        survey = Survey_System()
        self.assertEqual(survey.create_survey(self.course),1)
        
    def test_function_survey_question_type(self):
        survey = Survey_System()
        questionClass = question()
        survey.create_survey(self.course)
        survey.add_question_survey(self.question,self.course, "mandatory")
        questionClass.question_type(self.question,self.course,self.type)
        
        self.assertEqual(questionClass.return_type(self.course),["TEXT"])
   

    def test_function_survey_question(self):
        survey = Survey_System()
        questionClass = question()
        survey.create_survey(self.course)
        survey.add_question_survey(self.question,self.course, "mandatory")
        questionClass.question_type(self.question,self.course,self.type)
        
        self.assertEqual(questionClass.return_question(self.course),["Hello what is your name"])
    
#######################################################################################################################################################################
#Tests for enrolment
    def test_nonexistant_course(self):
        control = Controller()
        courses = control.course_list(self.semester)
        self.assertFalse((self.course in courses))
        
    def test_non_enrolled_course(self):
        control = Controller()
        details = control.search_enrolments(self.realUser)
        self.assertFalse(self.course in details)
    def test_non_existent_user(self):
        control = Controller()
        details = control.search_userdata(self.user)

        self.assertEqual(details, "ERROR")

#######################################################################################################################################################################
#Tests for optional and mandatory questions
    def test_function_optional_add(self):
         admin = administrator()
         survey = Survey_System()
         admin.add_optional_question(self.question)
         details = survey.return_optional_pool()
         #print(details)
         
         self.assertEqual(details[len(details)-1],"Hello what is your name")
        
         
    def test_optional_pool_delete(self):
         admin = administrator()
         survey = Survey_System()
         admin.add_optional_question(self.question)
         admin.del_optional_question(self.question)
         details = survey.return_optional_pool()

         self.assertFalse(details[len(details)-1] == "Hello what is your name")

    def test_optional_false_deletion(self):
        admin = administrator()
        survey = Survey_System()
        preDeletion = survey.return_optional_pool()
        admin.del_optional_question(self.falseQuestion)
        postDeletion = survey.return_optional_pool()

        self.assertEqual(preDeletion,postDeletion)
    
    def test_function_mandatory_add(self):
         admin = administrator()
         survey = Survey_System()
         admin.add_question_pool(self.question)
         details = survey.return_pool()
         #print(details)
         
         self.assertEqual(details[len(details)-1],"Hello what is your name")
        
         
    def test_mandatory_pool_delete(self):
         admin = administrator()
         survey = Survey_System()
         admin.add_question_pool(self.question)
         admin.del_question_pool(self.question)
         details = survey.return_pool()

         self.assertFalse(details[len(details)-1] == "Hello what is your name")

    def test_mandatory_false_deletion(self):
        admin = administrator()
        survey = Survey_System()
        preDeletion = survey.return_pool()
        admin.del_question_pool(self.falseQuestion)
        postDeletion = survey.return_pool()

        self.assertEqual(preDeletion,postDeletion)
#######################################################################################################################################################################
#Tests for Results collection
    def test_results_add(self):
        answerClass = answer()
        survey = Survey_System()
        answerClass.input_answer(self.course, self.questionNumber, self.question, self.answer, self.type)
        result = answerClass.return_results(self.course)
        self.assertEqual(result[0].answer, "My name is John Doe")
        
    def test_completed_survey(self):
        survey = Survey_System()
        survey.add_finished(self.course, self.user)
        control = Controller()
        results = control.search_completed(self.user)
        self.assertEqual(results[0],"COMP9999 17s2")
#####################################################################################################################################################################
#Tests for Opening Surveys

    def test_survey_open(self):
        
        admin = administrator()
        admin.close_survey(self.course2)
        studentClass = student()
        #print(studentClass.return_open_surveys())
        prelist = studentClass.return_open_surveys()
        admin.open_survey(self.course2, self.start_date, self.start_time, self.end_date, self.end_time)
        postlist = studentClass.return_open_surveys()
        #print(studentClass.return_open_surveys())

        self.assertFalse(prelist == postlist)
        self.assertTrue(len(prelist) == len(postlist)-1)
        admin.close_survey(self.course2)
        
        #print(studentClass.return_open_surveys())
    def test_survey_close(self):
        
        admin = administrator()
        admin.open_survey(self.course2, self.start_date, self.start_time, self.end_date, self.end_time)
        studentClass = student()
        #print(studentClass.return_open_surveys())
        prelist = studentClass.return_open_surveys()
        admin.close_survey(self.course2)
        postlist = studentClass.return_open_surveys()
        #print(studentClass.return_open_surveys())

        self.assertFalse(prelist == postlist)
        self.assertTrue(len(prelist) == len(postlist)+1)
        admin.close_survey(self.course2)
        
            
######################################################################################################################################################################
#Run the test-cases
if __name__ == '__main__':
 unittest.main(verbosity = 5)


