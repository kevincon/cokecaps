from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


class capbot:
	def __init__(self, e, pw):
		self.email = e
		self.password = pw
	
	def __init__(self):
		self.email = "null"
		self.password = "null"

	def get_email(self):
		return self.email

	def get_password(self):
		return self.password

	def set_email(self, e):
		self.email = e

	def set_password(self, pw):
		self.password = pw
	
	def log_in(self):	
		# Create a new instance of the Firefox driver
		driver = webdriver.Firefox()
	
		# go to MCR
		driver.get("http://www.mycokerewards.com")

		# find email field and enter email
		inputElement = driver.find_element_by_id("emailAddress")
		inputElement.send_keys("4biddensodaluv@gmail.com")
		#inputElement.send_keys(self.email)

		# find password field and enter password
		inputElement = driver.find_element_by_id("passwordText")
		inputElement.send_keys("sodaluver")
		#inputElement.send_keys(self.password)

		# submit the log-in information
		inputElement.submit()

		#Wait and see if the user logged in successfully
		try:
			element = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_link_text("Sign Out"))
			return True
		except (ElementNotVisibleException, ElementNotSelectableException):
			return False

	def enter_code(self, code):
		
	
	def log_out(self):
		#code goes here
