import sqlite3
from sqlalchemy import Table, Column, ForeignKey, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import datetime
from time import gmtime, strftime
engine = create_engine('sqlite:///results.db')
completedEngine = create_engine('sqlite:///completed.db')
Base = declarative_base()
completedBase = declarative_base()
"""
Precondition of running this program: Run Library.py for once
The MVC architecture which allows the user to query the library by book's name and also
author's name
"""
# Controller module
# Ben's code integrated
class Survey_System(object):
    def __init__(self):
        pass

    def create_survey(self, course):
        method = SurveyMethod()
        add = method.create_survey(course)
        return add
    
    def create_results(self):
        method = SurveyMethod()
        add = method.create_results()
    
    def create_finished(self):
        method = SurveyMethod()
        add = method.create_finished()

    def add_question_survey(self, question, course, type):
        method = SurveyMethod()
        add = method.add_question_survey(question, course, type)

    def survey_q(self, course):
        method = SurveyMethod()
        data = method.survey_q(course)
        return data

    def return_pool(self):
        method = SurveyMethod()
        data = method.return_pool()
        return data

    def return_optional_pool(self):
        method = SurveyMethod()
        data = method.return_optional_pool()
        return data

    def question_type(self, question, course, type):
        method = SurveyMethod()
        add = method.question_type(question, course, type)

    def return_type(self, course):
        method = SurveyMethod()
        data = method.return_type(course)
        return data
    
    def return_question(self, course): #Question
        method = SurveyMethod()
        data = method.return_question(course)
        return data

    def input_answer(self, course,questionNumber,question,answer, Qtype):
        method = SurveyMethod()
        data = method.input_answer(course, questionNumber,question,answer, Qtype)
        
        if(data):
            return 1 #if successful return 1 , else return -1
        else:
            return -1
        
    def add_finished(self, course, username):
        method = SurveyMethod()
        add = method.add_finished(course,username)

class administrator(object):
    def __init__(self):
        pass

    def add_question_pool(self, question):
        method = SurveyMethod()
        add = method.add_question_pool(question)

    def del_question_pool(self, question):
        method = SurveyMethod()
        add = method.del_question_pool(question)

    def add_optional_question(self, question):
        method = SurveyMethod()
        add = method.add_optional_question(question)

    def del_optional_question(self, question):
        method = SurveyMethod()
        add = method.del_optional_question(question)

    def close_survey(self, course):
        method = SurveyMethod()
        add = method.close_survey(course) 

    def open_survey(self, course, start_date, start_time, end_date, end_time):
        method = SurveyMethod()
        add = method.open_survey(course, start_date, start_time, end_date, end_time)        

    def return_results(self, course): #Answer
        method = SurveyMethod()
        data = method.return_results(course)
        return data

class staff(object):
    def __init__(self):
        pass

    def add_optional_question(self, question):
        method = SurveyMethod()
        add = method.add_optional_question(question)

    def del_optional_question(self, question):
        method = SurveyMethod()
        add = method.del_optional_question(question)

    def return_review_survey(self):
        method = SurveyMethod()
        data = method.return_review_survey()
        return data

class student(object):
    def return_open_surveys(self):
        method = SurveyMethod()
        data = method.return_open_surveys()
        return data

    def return_all_surveys(self):
        method = SurveyMethod()
        data = method.return_all_surveys()
        return data

class question(object):
    def question_type(self, question, course, type): #Question
        method = SurveyMethod()
        add = method.question_type(question, course, type)

    def return_type(self, course): #Question
        method = SurveyMethod()
        data = method.return_type(course)
        return data

    def return_question(self, course): #Question
        method = SurveyMethod()
        data = method.return_question(course)
        return data
    
class answer(object):
    def return_results(self, course): #Answer
        method = SurveyMethod()
        data = method.return_results(course)
        return data
    
    def input_answer(self, course,questionNumber,question,answer,Qtype): #Answer
        method = SurveyMethod()
        data = method.input_answer(course, questionNumber,question,answer,Qtype)
        
        if(data):
            return 1 #if successful return 1 , else return -1
        else:
            return -1

# Model
#Ben's code Integrated
class SurveyMethod(object):
    def add_question_pool(self, question):                             
        query = "REPLACE INTO POOLQUESTION (QUESTION) VALUES ('%s')" %question
        result = self._dbselect(query, "pool.db")

    def del_question_pool(self, question):
        query = "DELETE from POOLQUESTION where QUESTION = '%s'" %question
        result = self._dbselect(query, "pool.db")

    def add_optional_question(self, question):
        query = "REPLACE INTO OPTIONALPOOL (QUESTION) VALUES ('%s')" %question
        result = self._dbselect(query, "pool.db")
    
    def del_optional_question(self, question):
        query = "DELETE from OPTIONALPOOL where QUESTION = '%s'" %question
        result = self._dbselect(query, "pool.db")

    def return_pool(self):
        query = "SELECT * from POOLQUESTION"
        result = self._dbselect(query, "pool.db")
        return result

    def return_optional_pool(self):
        query = "SELECT * from OPTIONALPOOL"
        result = self._dbselect(query, "pool.db")
        return result

    def create_survey(self, course):
        query = "CREATE TABLE IF NOT EXISTS '%s' (QUESTION TEXT PRIMARY KEY NOT NULL, TYPE TEXT, POOLTYPE TEXT)" %course
        result = self._dbselect(query, "survey.db")
        query = "REPLACE INTO STAGE (COURSE, STATUS, STARTDATE, STARTTIME, ENDDATE, ENDTIME) VALUES('%s', 'REVIEW', '00', '00', '00', '00')" % course
        result = self._dbselect(query, "surveyStage.db")
        return 1

    def add_question_survey(self, question, course, type):
        query = "REPLACE INTO '%s' (QUESTION) VALUES ('%s')" %(course, question)  
        result = self._dbselect(query, "survey.db")
        query = "UPDATE '%s' SET POOLTYPE = '%s' where QUESTION = '%s'" %(course, type, question)
        result = self._dbselect(query, "survey.db")
        query = "UPDATE '%s' SET TYPE = 'NIL' where QUESTION = '%s'" %(course, question)
        result = self._dbselect(query, "survey.db")

    def survey_q(self, course):
        query = "SELECT count(*) from sqlite_master where type='table' and name='%s'" %course
        result = self._dbselect(query, "survey.db")
        if result == [1]:
            query = "SELECT QUESTION from '%s' where type = 'NIL'" % course
            result = self._dbselect(query, "survey.db")
            return result
        else:
            return []

    def question_type(self, question, course, type):
    	query = "UPDATE '%s' SET TYPE = '%s' where QUESTION = '%s'" %(course, type, question)
    	result = self._dbselect(query, "survey.db")

    def return_type(self, course):
    	query = "SELECT TYPE from '%s'" % course
    	result = self._dbselect(query, "survey.db")
    	return result

    def return_question(self, course): #Question
    	query = "SELECT QUESTION from '%s'" % course
    	result = self._dbselect(query, "survey.db")
    	return result 

    def return_review_survey(self):
        query = "SELECT * from STAGE where STATUS = 'REVIEW'"
        result = self._dbselect(query, "surveyStage.db")
        return result

    def close_survey(self, course):
        query = "UPDATE STAGE SET STATUS = 'CLOSED' where COURSE = '%s'" % course
        result = self._dbselect(query, "surveyStage.db")

    def open_survey(self, course, start_date, start_time, end_date, end_time):
        query = "REPLACE INTO STAGE (COURSE, STATUS, STARTDATE, STARTTIME, ENDDATE, ENDTIME) VALUES ('%s', 'OPEN', '%s', '%s', '%s', '%s')" %(course, start_date, start_time, end_date, end_time)
        result = self._dbselect(query, "surveyStage.db")

    def return_open_surveys(self):
        query = "SELECT * FROM STAGE where STATUS = 'OPEN'"
        result = self._dbselect(query, "surveyStage.db")
        return result

    def return_all_surveys(self):
        query = "SELECT COURSE FROM STAGE"
        result = self._dbselect(query, "surveyStage.db")
        return result

    def create_results(self):
        try:
            Base.metadata.create_all(engine)
        except:
            print("Table already exists.")
        
    def return_results(self, course): #Answer
        DBSession = sessionmaker(bind = engine)
        session = DBSession()
        results = session.query(Answer).filter(Answer.course == course)
        #session.close()
        return results

    def input_answer(self, course, questionNumber,question, answer, Qtype):
        DBSession = sessionmaker(bind = engine)
        session = DBSession()
        currentAnswer = Answer(course = course, questionNumber = questionNumber ,question = question, answer = answer, Qtype = Qtype)
        session.add(currentAnswer)
        session.commit()
        session.close()
        
    def create_finished(self):
        try:
            completedBase.metadata.create_all(completedEngine)
        except:
            print("Table already exists.")
    
    def add_finished(self, course, username):
        DBSession = sessionmaker(bind = completedEngine)
        session = DBSession()
        currentCompleted = completedSurvey(username = username,course = course)
        session.add(currentCompleted)
        session.commit()
        session.close()

    def _dbselect(self, query, database):
    # Logic to connect to the database. Students will be introduced to this
    # in the lectures this week
        connection = sqlite3.connect(database)     #Opens a connection to the SQLite database file database
        cursorObj = connection.cursor()                #creates a cursor object used for pointing at objects
 
    # execute the query
        rows = cursorObj.execute(query)                #execute allows you to return another cursor object or execute SQL commands
        connection.commit()                            #writes the data to the database

        results = []                                   #returns the result into this list
        if not rows:
            return results
        else:
            for row in rows:
                results.append(row[0])
            cursorObj.close()
            return results

class Answer(Base):
    __tablename__ = "Answers"
    id = Column(Integer, primary_key = True)
    course = Column(String)
    questionNumber = Column(Integer, nullable = False)
    question = Column(String)
    answer = Column(String)
    Qtype = Column(String)

class completedSurvey(completedBase):
    __tablename__ = "CompletedSurveys"
    id = Column(Integer,primary_key = True)
    username = Column(Integer, nullable = False)
    course = Column(String)

system = Survey_System()
system.create_results()
system.create_finished()
"""
#Client Code
admin = administrator()
admin.add_question_pool("Hello who are you?")
system = Survey_System()
a = system.return_pool()
print(a)
"""
"""
staff = staff()
a = staff.return_review_survey()
for cour in a:
	print(cour)
"""
