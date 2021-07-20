from flask import Flask, redirect, render_template, request, url_for
from server import app
from surveyF import *
from members import Admin, admin1, User
from mvc import Controller, LibraryModel
import csv
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from server import app,login_manager
from functools import wraps
from pie import *

#Prog v2
active_course = "no_course_selected"
access_role = ""
username = 0     #global username so it can you used throughout all the functions
global_surveys = []
question = ""

#INITIAL LOGIN PAGE


#-------------- Wrapper for role management and page direction---------------
def required_roles(*roles):
	def wrapper(f):
		@wraps(f) 
		def wrapped(*args, **kwargs):
			if get_current_user_role(username) not in roles:
				return redirect(url_for('_401'))
			return f(*args, **kwargs)
		return wrapped
	return wrapper

#----------- unauthorised access to a page -------------
@app.route('/401')
def _401():
	return render_template("unauthorised.html")

def get_current_user_role(userame):
	controller = Controller()
	return controller.search_role(username)

#--------------- checks password with the one in the database -----------------
def check_password(username, password):
	controller = Controller()
	access_login = controller.login_credential(username, password)
	if access_login == 1:							#returns 1 if right, 0 if wrong
		user = User(username)						#returns the username
		login_user(user)
		return True
	return False

#------ get the user details-----------
def get_user(username):
	controller = Controller()
	access_user = controller.search_userdata(username) 
	return User(username)
	
#---------- initialising the login session with the user details -------------------
@login_manager.user_loader
def load_user(username):    
	user = get_user(username)
	return user

@app.route("/", methods=["GET", "POST"])
def index():
	login = 0
	if request.method == "POST":
		global username
		global access_role                                                      #while login not successful
		username = int(request.form["username"])
		password = request.form["password"]
		controller = Controller()
		access_login = controller.login_credential(username, password)      #returns 1 if right 0 if wrong
		access_user = controller.search_userdata(username)                  #returns the username

		access_role = controller.search_role(username)
		if check_password(username, password):								#this redirects them to the correct dash
			if access_role == "admin":
				return redirect(url_for('adminDashBoard'))
			elif access_role == "staff":
				return redirect(url_for('staffDashBoard'))
			elif access_role == "student":
				return redirect(url_for('studentDashBoard'))                          #successful, render home page
	return render_template("login.html")

#----------------Dashboard for all 3 uer types (Provides the gate to other functions of the survey)-----------------------
@app.route("/adminDashBoard", methods=["GET", "POST"])
@required_roles('admin')
@login_required
def adminDashBoard():
	if request.method == "POST":
		button = request.form["button"]
		if button == "Pool":
			return redirect(url_for("poolChoice"))
		elif button == "SeeSurvey":
			return redirect(url_for("staffSurveyList"))
		elif button == "OPENCLOSE":
			return redirect(url_for("openClose"))
		elif button == "CREATE":
			return redirect(url_for("create"))
		elif button == "METRIC":
			return redirect(url_for("metric"))
	return render_template("adminDashBoard.html")

@app.route("/staffDashBoard", methods=["GET", "POST"])
@required_roles('staff')		#new decorator for the page view
@login_required
def staffDashBoard():
	if request.method == "POST":
		button = request.form["button"]
		if button == "Pool":
			return redirect(url_for("optionalPool"))
		elif button == "SeeSurvey":
			return redirect(url_for("staffSurveyList"))
		elif button == "CREATE":
			return redirect(url_for("create"))
		elif button == "METRIC":
			return redirect(url_for("metric"))
	return render_template("staffDashBoard.html")

@app.route("/studentDashBoard", methods=["GET", "POST"])
@required_roles('student')
@login_required
def studentDashBoard():
	if request.method == "POST":
		button = request.form["button"]
		if button == "fill":
			return redirect(url_for("studentSurveyList"))
		elif button == "METRIC":
			return redirect(url_for("metric"))
	return render_template("studentDashBoard.html")

#===========================================================================
#================Shows the graph of the result =========================
@app.route("/metric", methods=["GET", "POST"])
@login_required
def metric():
	global question
	pieChart = ""
	if question and active_course:
		pieChart = pie(active_course, question)
	if request.method == "POST":
		button = request.form["button"]
		if button == "back":
			question = ""
			if access_role == "admin":
				return redirect(url_for("adminDashBoard"))
			elif access_role == "staff":
				return redirect(url_for("staffDashBoard"))
			elif access_role == "student":
				return redirect(url_for("studentDashBoard"))
		elif button == "GRAPH":
			return redirect(url_for("metricChoose"))
	return render_template("metric.html", pieChart=pieChart)	
#========================================================================
@app.route("/metricChoose", methods=["GET", "POST"])
@login_required
def metricChoose():
	global active_course
	if request.method == "POST":
		button = request.form["button"]
		print(button)
		if button == "back":
			return redirect(url_for("metric"))
		elif button == "choose":
			active_course = request.form["course"]
			return redirect(url_for("metricQuestion"))
	return render_template("metricChoose.html", al = return_all_surveys())

def return_all_surveys():
	stu = student()
	al = stu.return_all_surveys()
	return al

def return_questi():
	survey =  Survey_System()
	al = survey.return_question(active_course)
	return al

@app.route("/metricQuestion", methods=["GET", "POST"])
@login_required
def metricQuestion():
	global active_course
	global question
	if request.method == "POST":
		button = request.form["button"]
		if button == "back":
			return redirect(url_for("metricChoose"))
		elif button == "create":
			question = request.form["question"]
			return redirect(url_for("metric"))
	return render_template("metricQuestion.html", al = return_questi())
#----------------Helper function for showing surveys in the review stage for admin-----------------------
def openCloseHelper():
	controller = Controller()
	retVal = controller.surveyStage()
	return retVal
#===========================================================================
#----------------show only surveys in review stage so that they can be opened or closed-----------------------
@app.route("/openClose", methods=["GET", "POST"])
@required_roles('admin')
@login_required
def openClose():
	if request.method == "POST":
		global global_surveys
		admin = administrator()
		global_surveys = request.form.getlist("courses")
		button = request.form["button"]
		if button == "open":
			return redirect(url_for("changeStatusOpen"))
		elif button == "back":
			return redirect(url_for("adminDashBoard"))
			return render_template("adminDashBoard.html")
		elif button == "close":
			for survey in global_surveys:
				admin.close_survey(survey)
			return redirect(url_for("openClose"))
			#return render_template("openClose.html", survey_status = openCloseHelper())
	return render_template("openClose.html", survey_status = openCloseHelper())
#===========================================================================
@app.route("/changeStatusOpen", methods=["GET", "POST"])
@required_roles('admin')
@login_required
def changeStatusOpen():
	if request.method == "POST":
		i = 0
		admin = administrator()
		button = request.form["button"]
		if button == "submit":
			start_date = request.form.getlist("STARTDATE")
			start_time = request.form.getlist("STARTTIME")
			end_date = request.form.getlist("ENDDATE")
			end_time = request.form.getlist("ENDTIME")
			for survey in global_surveys:
				admin.open_survey(survey, start_date[i], start_time[i], end_date[i], end_time[i])
				i += 1
			#return redirect(url_for("openClose"))
			return redirect(url_for("openClose"))
			return render_template("openClose.html", survey_status = openCloseHelper())
		elif button == "back":
			if access_role == "admin":
				return redirect(url_for("openClose"))
				return render_template("openClose.html", survey_status = openCloseHelper())
			elif access_role == "staff":
				return redirect(url_for("staffSurveyList"))
				return render_template("staffSurveyList.html", all_surveys = review_survey())
	return render_template("openSurveys.html", surveys = global_surveys)            
	#return render_template("openClose.html", survey_status = openCloseHelper())

@app.route("/create", methods=["GET", "POST"])
@required_roles('admin','staff')
@login_required
def create():
	if request.method == "POST":
		global active_course
		active_course = request.form["course"]
		button = request.form["action"]
		if button == "create":
			return redirect(url_for("poolChoiceSurvey"))
		elif button == "back":
			if access_role == "admin":
				return redirect(url_for("adminDashBoard"))
				return render_template("adminDashBoard.html")
			elif access_role == "staff":
				return redirect(url_for("staffDashBoard"))
				return render_template("staffDashBoard.html")
	return render_template("create.html", courses = subject())

@app.route("/poolChoiceSurvey", methods=["GET", "POST"])
@required_roles('staff','admin')
@login_required
def poolChoiceSurvey():
	if request.method == "POST":
		button = request.form["button"]
		if button == "optional":
			return redirect(url_for("addOptionalPool"))
		elif button == "mandatory":
			return redirect(url_for("pool"))
		elif button == "back":
			return redirect(url_for("create"))
	return render_template("poolChoice.html")   

@app.route("/poolChoice", methods=["GET", "POST"])
@required_roles('admin','staff')
@login_required
def poolChoice():
	if request.method == "POST":
		button = request.form["button"]
		if button == "optional":
			return redirect(url_for("optionalPool"))
		elif button == "mandatory":
			return redirect(url_for("home"))
		elif button == "back":
			return redirect(url_for("adminDashBoard"))
			return render_template("adminDashBoard.html")
	return render_template("poolChoice.html")   

#----------------Helper function for showing surveys in the review stage for staff-----------------------
def review_survey():
	staffq =  staff() 
	surveys = staffq.return_review_survey()
	return surveys
#===========================================================================

#----------------show only surveys in review stage (used in conjunction with review_survey()) -----------------------
@app.route("/staffSurveyList", methods=["GET", "POST"])
@required_roles('admin','staff')
@login_required
def staffSurveyList():
	global active_course
	global global_surveys
	if request.method == "POST":
		button = request.form["button"]
		if button == "back":
			if access_role == "staff":
				return redirect(url_for("staffDashBoard"))
				return render_template("staffDashBoard.html")
			elif access_role == "admin":
				return redirect(url_for("adminDashBoard"))
				return render_template("adminDashBoard.html")
		elif button == "see_survey":
			active_course = request.form["course"]
			return redirect(url_for("survey"))
	return render_template("staffSurveyList.html", all_surveys = review_survey())
#===========================================================================

def subject():
	controller = Controller() 
	subj_list1 = controller.course_list("17s2")
	subj_list2 = controller.course_list("18s1")
	subj_list3 = controller.course_list("18s2")
	subj_final = subj_list1 + subj_list2 + subj_list3
	return subj_final

#===============  shows the surveys for that the student is enrolled in========
#==============used in conjunction with enrolment==============
@app.route("/studentSurveyList", methods=["GET", "POST"])
@required_roles('student')
@login_required
def studentSurveyList():
	global active_course
	if request.method == "POST":
		button = request.form["button"]
		if button == "answer_questions":
			active_course = request.form["course"]
			return redirect(url_for("survey"))
		elif button == "back":
			return redirect(url_for("studentDashBoard"))
			return render_template("studentDashBoard.html")
	return render_template("studentSurveyList.html", all_enrolments = enrolment(), idStudent = username)
#========================================================================================

#=================Helper function returns a list of enrolements for a particular====
#=================username student=======================
def enrolment(): #Ben's code integrated
	final_list = []
	controller = Controller() 
	enrolment_list = controller.search_enrolments(username)
	finished_list = controller.search_completed(username)
	stu = student()
	open_surveys = stu.return_open_surveys()
	for enrolment in enrolment_list:
		if enrolment in open_surveys and enrolment not in finished_list:
			final_list.append(enrolment)

	return final_list
#========================================================================================

@app.route("/loadStudentSurvey", methods=["GET", "POST"])
@required_roles('student')
@login_required
def loadStudentSurvey():
	if request.method == "POST":
		button = request.form["button"]
		if button == "answer_survey":
			return redirect(url_for("loadStudentSurvey"))
	return render_template("loadStudentSurvey.html")

#==========================Helper function that reutrns a list filled with =====
# =========================questions from the mandatory question pool=====
def return_pool():
	question_pool = []
	system = Survey_System()
	question_pool = system.return_pool()
	if not question_pool:
		return []
	else:
		return question_pool
#==========================Helper function that reutrns a list filled with ===========
#========================== questions from the optional question pool=========
def return_optional_pool():
	question_pool = []
	system = Survey_System()
	question_pool = system.return_optional_pool()
	if not question_pool:
		return []
	else:
		return question_pool
#==============Is the mandatory pool page(you can add questions but not yet deleted)=====
#===============Used only for admins=========================
@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
	if request.method == "POST":
		global active_course
		active_course = request.form["question_name"]
		question = request.form["question_name"]
		if question == "back":
			return redirect(url_for("poolChoice"))
			return render_template("poolChoice.html")
		elif question == "edit":
			return redirect(url_for("editPool"))
			return render_template("pool.html", all_users=return_pool(), create_or_edit = "delete")
		else:   
			admin = administrator()
			admin.add_question_pool(question)
			return redirect(url_for("home"))
	return render_template("home.html", all_users=return_pool(), courses=subject())
#========================================================================================

#==============Allows you to delete questions from a pool=====
@app.route("/deleteQuestion", methods=["GET", "POST"])
@login_required
def editPool():
	if request.method == "POST":
		i = 0
		button = request.form["button"]
		if button == "delete":
			checked_questions = request.form.getlist("questions")
			admin = administrator()
			while i < len(checked_questions):
				admin.del_question_pool(checked_questions[i])
				i+=1
		elif button == "back":
			return redirect(url_for("home"))
			return render_template("home.html", all_users=return_pool(), courses=subject())
	return render_template("pool.html", all_users=return_pool(), create_or_edit = "delete")
#========================================================================================

#==============Allows you to delete questions from a pool=====
@app.route("/deleteOptionalQuestion", methods=["GET", "POST"])
@required_roles('staff', 'admin')
@login_required
def editOptionalPool():
	i = 0
	if request.method == "POST":
		button = request.form["button"]
		if button == "back":
			if access_role == "admin":
				return redirect(url_for("optionalPool"))
			elif access_role == "staff":
				return redirect(url_for("optionalPool"))

		if button == "delete":
			checked_questions = request.form.getlist("questions")
			admin = administrator()
			while i < len(checked_questions):
				admin.del_optional_question(checked_questions[i])
				i+=1
	return render_template("pool.html", all_users=return_optional_pool(), create_or_edit = "delete")
#========================================================================================
@app.route("/addOptionalQuestion", methods=["GET", "POST"])
@required_roles('staff', 'admin')
@login_required
def addOptionalPool():
	i = 0
	if request.method == "POST":
		button = request.form["button"]
		if button == "back":
			if access_role == "admin":
				return redirect(url_for("poolChoiceSurvey"))
			elif access_role == "staff":
				return redirect(url_for("optionalPool"))

		if button == "create":
			checked_questions = request.form.getlist("questions")
			system = Survey_System()
			system.create_survey(active_course)
			while i < len(checked_questions):
				system.add_question_survey(checked_questions[i], active_course, "optional")
				i+=1
			return redirect(url_for("mcqOrText"))
	return render_template("pool.html", all_users=return_optional_pool(), create_or_edit = "create")
#==============Is the optional pool page(you can add questions but not yet deleted)=====
#===============Used for admins and staff=========================
@app.route("/optionalPool", methods=["GET", "POST"])
@required_roles('staff', 'admin')
@login_required
def optionalPool():
	if request.method == "POST":
		global active_course
		global access_role
		active_course = request.form["question_name"]
		question = request.form["question_name"]
		if question == "back":
			if access_role == "admin":
				return redirect(url_for("poolChoice"))
				return render_template("poolChoice.html")   
			elif access_role == "staff":
				return redirect(url_for("staffDashBoard"))
				return render_template("staffDashBoard.html")
		elif question == "edit":
			return redirect(url_for("editOptionalPool"))
			return render_template("pool.html", all_users=return_optional_pool(), create_or_edit = "delete")
		else:   
			admin = administrator()
			admin.add_optional_question(question)
			return redirect(url_for("optionalPool"))
	return render_template("home.html", all_users=return_optional_pool(), courses=subject())
#========================================================================================

#========Is used to create the survey give a list of pool question then you select it====
#========Currently only works for mandatory pool ===============
@app.route("/Pool",methods=["GET", "POST"])
@required_roles('admin')
@login_required
def pool():
	i = 0
	if request.method == "POST":
		button = request.form["button"]
		if button == "back":
			if access_role == "admin":
				return redirect(url_for("poolChoiceSurvey"))
			elif access_role == "staff":
				return redirect(url_for("optionalPool"))

		if button == "create":
			checked_questions = request.form.getlist("questions")
			system = Survey_System()
			system.create_survey(active_course)
			while i < len(checked_questions):
				system.add_question_survey(checked_questions[i], active_course, "mandatory")
				i+=1
			return redirect(url_for("mcqOrText"))
	return render_template("pool.html", all_users=return_pool(), create_or_edit = "create")
#========================================================================================

#=====Is a page that allows you to choose whether a question=====
#=====should be answered in mcqOrText========================
@app.route("/mcqOrText",methods=["GET", "POST"])
@required_roles('staff', 'admin')
@login_required
def mcqOrText():
	i = 0
	system = Survey_System()
	if request.method == "POST":
		survey = return_survey()
		for question in survey:
			form_name = question
			type = request.form[form_name]
			system.question_type(question, active_course, type)
									#this redirects them to the correct dash
		if access_role == "admin":
			return redirect(url_for('adminDashBoard'))
		elif access_role == "staff":
			return redirect(url_for('staffDashBoard'))
	return render_template("mcqOrText.html", questions=return_survey())

#============Helper function that returns question=======
#============Doesn't return the type only question=============
#============Questions should be in the same order the as type=========
#======Used in conjunction with return_type()=====================
def return_survey():
	q = []
	system = Survey_System()
	q = system.survey_q(active_course)
	return q
#============Helper function that returns the type of the question=======
#============Doesn't return the questions only returns type=============
#============Questions should be in the same order the as type=========
def return_type():
	q = []
	system = Survey_System()
	q = system.return_type(active_course)
	return q

#===========Shows the survey either in MCQ or TEXT=============
#====Used in conjunction with return_type() and ()
@app.route("/Survey", methods=["GET", "POST"])
@required_roles('student','admin','staff')
@login_required
def survey(): #Ben's code integrated here
	controller = Controller()
	questionList = controller.question_and_type(active_course)
	if request.method == "POST":
		i = 0
		questionList = controller.question_and_type(active_course)
		system = Survey_System()
		system.create_results()
		system.create_finished()
		while i < len(questionList):#while i less than number of questions in survey
			CurrentQuestion = questionList[i]  
			questionNum = i + 1
			question = CurrentQuestion[0]
			answer = request.form[CurrentQuestion[0]]
			
			system.input_answer(active_course,questionNum,question,answer, CurrentQuestion[1])
			i+=1
		system.add_finished(active_course,username)
		return redirect(url_for('studentDashBoard'))
	button_list = ['1','2', '3', '4','5']   
	return render_template("survey.html", all_users = controller.question_and_type(active_course), type = return_type(), b=button_list)  

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))


