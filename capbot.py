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
	
	#def __init__(self):
	#	self.email = "null"
	#	self.password = "null"
	#	self.driver = webdriver.Firefox()

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
		self.driver.get("http://www.mycokerewards.com")

		# find email field and enter email
		inputElement = self.driver.find_element_by_id("emailAddress")
		#inputElement.send_keys("4biddensodaluv@gmail.com")
		inputElement.send_keys(self.email)

		# find password field and enter password
		inputElement = self.driver.find_element_by_id("passwordText")
		#inputElement.send_keys("sodaluver")
		inputElement.send_keys(self.password)

		# submit the log-in information
		inputElement.submit()

		#Wait and see if the user logged in successfully, want to be able to wait, and determine if log-in failed by using
			#self.driver.find_element_by_class_name("balloonErrorBody")
			#self.driver.find_element_by_id("loginForm")
		try:
			element = WebDriverWait(self.driver, 10).until(lambda driver : self.driver.find_element_by_link_text("Sign Out"))

		
		except (ElementNotSelectableException, ElementNotVisibleException, TimeoutException):
			raise LoginError('Incorrect login information')

		#except:
		#	raise InternetError('Login timed out, try again later')

	def enter_code(self, code):
		#enter code into field
		codeInput = self.driver.find_element_by_id("rewardCode")
		codeInput.send_keys(code)
		codeInput.submit()
		
		#close the dialog box that opens when entering a code
		self.driver.implicitly_wait(5)
		self.driver.refresh()
		#self.driver.find_elements_by_tag_name("a").click()
		
	
	def log_out(self):
		#preconditions: main page showing, regular screen immediately after log-in must be showing, NO ERROR BUBBLE, NO ENTER CODE BUBBLE
		#sign out
		element = self.driver.find_element_by_link_text("Sign Out")
		element.click()

		#close browser window
		self.driver.close()


test = capbot('4biddensodaluv@gmail.com', 'sodaluver')
try:
	retval = test.log_in()
except LoginError, e:
	print "".join(e.args)
except InternetError, j:
	print "".join(j.args)
test.enter_code("v674ppv4x770k5")
test.log_out()
print "done"
#finally:
#	test.log_out()
