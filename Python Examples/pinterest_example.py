import unittest
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from datetime import date

class MyTestCase(unittest.TestCase):

	def setUp(self):
	#this is where set up for the test is done. This will usually contain code to create a new browser window
	
		#uncomment the two below lines to run test on remote server
        #remoteHost = os.environ['HOST_IP']
        #self.selenium = webdriver.Remote(command_executor='http://'+remoteHost+':4444/wd/hub',desired_capabilities=webdriver.DesiredCapabilities().CHROME)
		
		#uncomment below lines to run locally in Chrome, you will need to download chromedriver.exe 
		#from https://sites.google.com/a/chromium.org/chromedriver/downloads and set the path to this file
		self.selenium = webdriver.Chrome('C:\Python34\chromedriver.exe')
		
		#uncomment below line to run locally in Firefox
		#self.selenium = webdriver.Firefox()

	def log_in(self, username, password):
		#For actions which take place multiple times, like logging in, define them in their own function 
		#this is an example of a function to log in 
		
		#Identify the email input box by its id tags
		emailaddressbox = self.selenium.find_element_by_id('userEmail')
		#sendkeys is used to type text into input boxes
		emailaddressbox.send_keys(username)
		
		#Type in a password too
		passwordbox = self.selenium.find_element_by_id('userPassword')
		passwordbox.send_keys(password)
		
		#Special keys like the Return key can also be sent
		passwordbox.send_keys(Keys.RETURN);
		
		#an implicit wait is where the code will wait a set time or until a condition is met
		#The find 'Friends to Follow' element is present on the page after logging in 
		#the line below waits either 20 seconds or until the find friends element is displayed
		WebDriverWait(self.selenium, 20).until(lambda s: s.find_element_by_id('friendsToFollow').is_displayed())

		return
		
		
	def test_stuff(self):
	#This function contains the main body of code for the test
	
		#The first thing this test does is navigate to site being tested.
		self.selenium.get('https://www.pinterest.com/')
		
		#Generally it can be a good idea to maximise the browser window too
		self.selenium.maximize_window()
		
		#As the test runs, it will have to wait for page elements to load, become visible, become active etc.
		#This can be done with implicit an explicit waits. Generally implicit waits should be used wherever possible
		#However there will be times where the site is awkward and using a short explicit wait can be easier
		
		#After navigating to the URL, the test will wait either 20 seconds for the email input box is displayed.
		#if the email input box is not displayed within 20 seconds, the test will fail.
		WebDriverWait(self.selenium, 20).until(lambda s: s.find_element_by_id('userEmail').is_displayed())
		
		#It is possible to tell the test to wait explicitly for set number of seconds regardless of what is displayed.
		#Generally its best to try avoid explicit waits as they can slow down the running of a test. 
		#However sometimes an explicit wait of 1 second can be the most efficient way of working around awkward page elements.  
		#below is an example of an explicit wait which waits for 2 seconds
		time.sleep(2)
	
		#functions can be called in the test, like the below call to the log_in function 
		self.log_in('justaseleniumtest@gmail.com','thisisatest')
		
		#As well as selecting page elements by their ids, it is possible to select them by css selector
		#The line below selects the element which has the <div class="usernameLink">
		username = self.selenium.find_element_by_css_selector(".usernameLink")
		
		#it can sometimes be useful to output text to the console,
		#This can be done using simple print statements
		print ('Successfully logged in : '+ str(username.text) +' is the username displayed on page')
		
		#When writing code to test code, various things can be tested using asserts.
		#An assert checks a statement and if that statement is not true, the test will fails and stop.
		
		#Below is a very basic Python assert that checks the correct username is displayed 
		#If it isn't displayed, the test will stop and the message specified will be displayed.
		assert(username.text == "justa"), "Unexpected username is displayed on page"
		
		#The below assert tests that some specific text is in the page title
		self.assertIn("Pinterest: discover and save creative ideas", self.selenium.title)
		
		#It is also possible to assert that things are not present 
		#like checking admin options are not present for non-admin users - which is an important test!
		#The below lines place the source code of the page into a variable named src 
		#and then checks that 'Error 404' is not present in the page source
		src = self.selenium.page_source
		self.assertNotIn("Error 404", src)
		
		#The lines below click on the conversation button, and wait for the menu to open
		button_to_click = self.selenium.find_element_by_xpath("html/body/div[1]/div[1]/div[2]/div[1]/div/button[1]").click()
		WebDriverWait(self.selenium, 20).until(lambda s: s.find_element_by_css_selector(".networkNotifDateHeader").is_displayed())
		
		#The test can then store the date displayed on the News tab in the variable news_date
		news_date = self.selenium.find_element_by_css_selector(".networkNotifDateHeader").text
		
		#convert this string into a datetime object
		news_date_time = datetime.strptime(news_date, "%A, %d %B %Y")
		print (news_date_time)
		
		#The test can compare date of news items to the current date, e.g check that.
		
		#get the current datetime
		now_date_time = datetime.now()


	
		
		
		if news_date_time < now_date_time:
			print('news date < now date')
		else:
			print('news dates is not < now date')
		if now_date_time > news_date_time:
			print ('now date > news date')
		else:
			print('now date is not > news date')
		
		
		
		
		
	
	def tearDown(self):
		#this is where all all the tidying up after the test is done. It's usually a good idea to close the browser window here.
		self.selenium.quit()
	

#The lines below are part of the unit test framework which tell Pytest to run the test 
if __name__=="__main__":
    unittest.main()
