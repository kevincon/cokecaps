from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

#Exceptions
class InternetError(Exception):
   def __init__(self, arg):
      self.args = 'Internet Error: ' + arg

class LoginError(Exception):
   def __init__(self, arg):
      self.args = 'Login Error: ' + arg

class BadCodeError(Exception):
   def __init__(self, arg):
      self.args = 'Bad Code Error: ' + arg

class PointLimitError(Exception):
   def __init__(self, arg):
      self.args = 'Point Limit Error: ' + arg

#Code Entering Automation
class capbot:
	def __init__(self, e, pw):
		self.email = e
		self.password = pw
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(5)
		self.points = 0

	def get_email(self):
		return self.email

	def get_password(self):
		return self.password

	def set_email(self, e):
		self.email = e

	def set_password(self, pw):
		self.password = pw
	
	def log_in(self):	
		# go to MCR
		self.driver.get("http://www.mycokerewards.com/home.do")

		# find email field and enter email
		inputElement = self.driver.find_element_by_id("emailAddress")
		inputElement.send_keys(self.email)

		# find password field and enter password
		inputElement = self.driver.find_element_by_id("passwordText")
		inputElement.send_keys(self.password)

		# submit the log-in information
		inputElement.submit()

		#Wait and see if the user logged in successfully
		try:
			element = WebDriverWait(self.driver, 10).until(lambda driver : self.driver.find_element_by_link_text("Sign Out"))

		
		except (ElementNotSelectableException, ElementNotVisibleException, TimeoutException):
			raise LoginError('Incorrect login information')
		#except:
		#	raise InternetError('Login timed out, try again later')
		

	def enter_code(self, code):
		pointsElement = self.driver.find_element_by_id("glPointsText")
		init_numPoints = pointsElement.text
		self.points = init_numPoints
		print init_numPoints
		
		#enter code into field
		codeInput = self.driver.find_element_by_id("rewardCode")
		codeInput.send_keys(code)
		codeInput.submit()
		
		
		
		
		#sign out
		signOut = self.driver.find_element_by_link_text("Sign Out")
		signOut.click()
		
		#sign back in
		try:
			self.log_in()
		except LoginError, e:
			print "".join(e.args)
		except InternetError, j:
			print "".join(j.args)
		
		#check new points number against old number
		pointsElement = self.driver.find_element_by_id("glPointsText")
		final_numPoints = pointsElement.text
		print final_numPoints
		
		#raises exception if the code did not get added to account...
		if self.points == final_numPoints:
			raise BadCodeError('Invalid Code Entered')
		#otherwise, sets value of self.points to new number of points
		else:
			self.points = final_numPoints
		
		
	
	def log_out(self):
		#preconditions: main page showing, regular screen immediately after log-in must be showing, NO ERROR BUBBLE, NO ENTER CODE BUBBLE
		
		#sign out
		element = self.driver.find_element_by_link_text("Sign Out")
		element.click()

		#close browser window
		self.driver.close()

#
#
#main test
#
#

test = capbot('4biddensodaluv@gmail.com', 'sodaluver')
try:
	test.log_in()
except LoginError, e:
	print "".join(e.args)
except InternetError, j:
	print "".join(j.args)
try:
	#test.enter_code("garbage")
	test.enter_code("6vt6blf6vm597n")
except BadCodeError, b:
	print "".join(b.args)
#test.log_out() #comment out for debugging and viewing the page so it doesn't just disappear!
print "done"



