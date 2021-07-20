import sqlite3
"""
Precondition of running this program: Run Library.py for once
The MVC architecture which allows the user to query the library by book's name and also
author's name
"""
# Controller module
class Controller(object):
 	def __init__(self):
 		pass
 	
 	def return_answers(self, course):
 		model = LibraryModel()	
 		userdata = model.return_answers(course)
 		return userdata 

 	def search_userdata(self, username):
 		model = LibraryModel()
 		userdata = model.search_userdata(username)
 		return userdata
 
 	def login_credential(self, username, password): 
 		model = LibraryModel()
 		passdata = model.login_credential(username, password) 		
 		return passdata

 	def search_role(self, username):
 		model = LibraryModel()
 		role = model.search_role(username)
 		return role
 	def search_completed(self, username):
 		model = LibraryModel()
 		completed = model.search_completed(username)
 		return completed 	

 	def search_enrolments(self, username):
 		model = LibraryModel()
 		enrolments = model.search_enrolments(username)
 		return enrolments

 	def course_list(self, semester):
 		model = LibraryModel()
 		course_list = model.course_list(semester)
 		return course_list

 	def question_and_type(self, course):
 		model = LibraryModel()
 		userdata = model.question_and_type(course)
 		return userdata

 	def surveyStage(self):
 		model = LibraryModel()
 		surveyStage = model.surveyStage()
 		return surveyStage

# Model
class LibraryModel(object):
	def login_credential(self, username, password):                             
 		query = "SELECT ID, PASSWORD, ROLE from LOGINDATA where ID = '%s'" % username
 		passdata = self._dbselect(query, "login.db")
 		if not passdata:
 			return 0
 		else:
 			retVal = passdata[0]
 			if retVal[0] == username and retVal[1] == password:
 				return 1
 			else:
 				return 0
 
	def search_userdata(self, username):
 		query = "SELECT ID, PASSWORD, ROLE from LOGINDATA where ID = '%s'" % username
 		userdata = self._dbselect(query, "login.db")
 		if not userdata:
 			return "ERROR"
 		else:
 			retVal = userdata[0]
 			return retVal[0]                                  
 
	def search_role(self, username):
		query = "SELECT ID, PASSWORD, ROLE from LOGINDATA where ID = '%s'" % username
		userdata = self._dbselect(query, "login.db")
		if not userdata:
			return "ERROR"
		else:
			retVal = userdata[0]
			return retVal[2] 

	def search_enrolments(self, username):
		query = "SELECT ID, COURSE, SEMESTER from STUENROLMENT where ID = '%s'" % username
		enrol = self._dbselect(query, "enrolments.db")
		if not enrol:
			return enrol
		else:
			retL = []
			for user in enrol:
				temp = user[1]+ " " + user[2]
				retL.append(temp)
		return retL

	def search_completed(self, username):
		query = "SELECT id, username, course from CompletedSurveys where username = '%s'" % username
		finished = self._dbselect(query, "completed.db")
		if not finished:
			return finished
		else:
			retL = []
			for user in finished:
				temp = user[2]
				retL.append(temp)
		return retL

	def course_list(self, semester):
		query = "SELECT COURSE, SEMESTER from SUBJECT where SEMESTER = '%s'" % semester
		subject_list = self._dbselect(query, "courses.db")
		if not subject_list:
			return subject_list
		else:
			ret = []
			for subject in subject_list:
				temp = subject[0] + " " + subject[1]
				ret.append(temp)
		return ret

	def question_and_type(self, course):                             
 		query = "SELECT * from '%s'" % course
 		retL = self._dbselect(query, "survey.db")
 		return retL 

	def surveyStage(self):                             
 		query = "SELECT * from STAGE"
 		retL = self._dbselect(query, "surveyStage.db")
 		return retL 

	def return_answers(self, course):
 		query = "SELECT * from Answers where COURSE = '%s'" %course
 		retL = self._dbselect(query, "results.db")
 		return retL 

	def _dbselect(self, query, database):
 	# Logic to connect to the database. Students will be introduced to this
 	# in the lectures this week
 		connection = sqlite3.connect(database)     #Opens a connection to the SQLite database file database
 		cursorObj = connection.cursor()                #creates a cursor object used for pointing at objects
 
 	# execute the query
 		rows = cursorObj.execute(query)  	           #execute allows you to return another cursor object or execute SQL commands
 		connection.commit()                            #writes the data to the database 
 		results = 0

 	# execute the query
 		rows = cursorObj.execute(query)  	           #execute allows you to return another cursor object or execute SQL commands
 		connection.commit()                            #writes the data to the database 
 		results = []                                   #returns the result into this list
 		for row in rows:
 			results.append(row)
 		cursorObj.close()
 		return results

"""
#Client Code
controller = Controller()
"""
"""
a = controller.search_passdata("staff670")
print(a)
a = controller.search_passdata("staff462")
print(a)
a = controller.search_userdata("1000")
print(a)
a = controller.search_userdata("51")
print(a)
a = controller.search_userdata("52")
print(a)
a = controller.search_userdata("53")
print(a)
a = controller.search_userdata("54")
print(a)
a = controller.search_role("50")
print (a)
a = controller.search_role("1932")
print (a)
a = controller.search_enrolments("100")
print (a)
"""
"""
a = controller.course_list("17s2")
print (a)
"""
