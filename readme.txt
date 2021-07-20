Section 1

matplotlib library needs to be installed
using (python3 -mpip install matplotlib) for homebrew python source from
https://matplotlib.org/faq/installing_faq.html

pld3 library needs to be installed
using (pip install mpld3) source from 
https://mpld3.github.io/install.html

sqlachemly library needs to be installed
using (pip(3) install SQLAlchemy)  source from
http://docs.sqlalchemy.org/en/latest/intro.html

the flask library needs to be installed
using (pip3 install flask) source from
https://stackoverflow.com/questions/24525588/how-to-install-flask-on-python3-using-pip

the flask-login library needs to be installed
using (pip3 install flask-login) source from
lab09 lab notes
Section 2
____________________________________________________________
To run the program, type "python3 run.py" in the terminal
while your in the directory of the programs

The url of the login page is http://127.0.0.1:8090/
____________________________________________________________
Section 3
The test can be carried out using "python3 tests.py"

All the test that are in the folder tests.zip which 
is in the python program test.py

In order
Test whether creation of survey is successful
def test_survey_creation_success(self):

Test whether question can be turned to a MCQ or text
def test_function_survey_question_type(self):

Test whether the function returns the correct question
def test_function_survey_question(self):

Tests whether the function returns correctly if a student is passed through a
non-existant course
def test_nonexistant_course(self):

Tests whether the function returns correctly if a student is passed through a
non-enrolled course
def test_non_enrolled_course(self):

Tests whether you can return information about a user that doesn't exist
def test_non_existent_user(self):

Tests whether adding a optional question is successful
def test_function_optional_add(self):

Tests whether deleting a optional question is successful
def test_optional_pool_delete(self):

Tests whether you can delete a fake question
def test_optional_false_deletion(self):

Tests whether adding a mandatory question is successful
def test_function_mandatory_add(self):

Tests whether deleting a mandatory question is successful
def test_mandatory_pool_delete(self):

Tests whether you can delete a fake question
def test_mandatory_false_deletion(self):

Tests whether you can a particular question
def test_results_add(self):

Tests whether after a user completes a quiz it goes into a 
completed database
def test_completed_survey(self):

Tests whether you can open a survey
def test_survey_open(self):

Tests whether you can close a survey
def test_survey_close(self):
