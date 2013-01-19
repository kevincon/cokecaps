from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

# go to the google home page
driver.get("http://www.mycokerewards.com")

# find the element that's name attribute is the input box
inputElement = driver.find_element_by_id("emailAddress")

# type in the search
inputElement.send_keys("4biddensodaluv@gmail.com")

# find the element that's name attribute is q (the google search box)
inputElement = driver.find_element_by_id("passwordText")
    
# type in the search 
inputElement.send_keys("sodaluver")

# submit the form (although google automatically searches now without submitting)
inputElement.submit()

#Wait and see if the user logged in successfully


try:
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
	element = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_link_text("Sign Out"))

	print driver.title

	inputElement = driver.find_element_by_id("rewardCode")
	inputElement.send_keys("AS12SKL2")
	inputElement.submit()
	driver.implicitly_wait(5)
	#inputElement.send_keys(userCode)

	#close the dialog box that opens when entering a code
	driver.find_elements_by_class_name("closeButton").click()

except #codeErrorPop.is_visible() :


finally:
        driver.get("http://www.google.com")




