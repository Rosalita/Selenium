import unittest
import calendar
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
	
		#Uncomment the two below lines to run this test on a remote server
		#remoteHost = os.environ['HOST_IP']
		#self.selenium = webdriver.Remote(command_executor='http://'+remoteHost+':4444/wd/hub',desired_capabilities=webdriver.DesiredCapabilities().CHROME)
		
		#Uncomment below lines to run the test locally in Chrome, you will need to download chromedriver.exe 
		#from https://sites.google.com/a/chromium.org/chromedriver/downloads and set the path to this file
		self.selenium = webdriver.Chrome('C:\Python34\chromedriver.exe')
		
		#Uncomment below line to run the test locally in Firefox
		#self.selenium = webdriver.Firefox()

	def log_in(self, username, password):
		#For actions which take place multiple times, like logging in, define them in their own function 
		#this is an example of a function to log in 
		
		#Identify the email input box by its id tags
		email_address_box = self.selenium.find_element_by_id('userEmail')
		#sendkeys is used to type text into input boxes
		email_address_box.send_keys(username)
		
		#Type in a password too
		password_box = self.selenium.find_element_by_id('userPassword')
		password_box.send_keys(password)
		
		#Special keys like the Return key can also be sent
		password_box.send_keys(Keys.RETURN)
		
		#An implicit wait is where the code will wait a set time or until a condition is met
		#The find 'Friends to Follow' element is present on the page after logging in 
		#The line below waits either 30 seconds or until the find friends element is displayed
		WebDriverWait(self.selenium, 30).until(lambda s: s.find_element_by_id('friendsToFollow').is_displayed())

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
		
		#After navigating to the URL, the test will wait either 30 seconds for the email input box is displayed.
		#If the email input box is not displayed within 30 seconds, the test will fail.
		WebDriverWait(self.selenium, 30).until(lambda s: s.find_element_by_id('userEmail').is_displayed())
		
		#It is possible to tell the test to wait explicitly for set number of seconds regardless of what is displayed.
		#Generally its best to try avoid explicit waits as they can slow down the running of a test. 
		#However sometimes an explicit wait of 1 second can be the most efficient way of working around awkward page elements.  
		#Below is an example of an explicit wait which waits for 2 seconds
		time.sleep(2)
	
		user_email = 'justaseleniumtest@gmail.com'
		
		#Functions can be called in the test, like the below call to the log_in function 
		self.log_in(user_email,'thisisatest')
		
		#As well as selecting page elements by their ids, it is possible to select them by css selector
		#The line below selects the element which has the <div class="usernameLink">
		username = self.selenium.find_element_by_css_selector(".usernameLink")
		
		#It can sometimes be useful to output text to the console,
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
		#Like checking admin options are not present for non-admin users - which is an important test!
		#The below lines place the source code of the page into a variable named src 
		#And then checks that 'Error 404' is not present in the page source
		src = self.selenium.page_source
		self.assertNotIn("Error 404", src)
			
		#The lines below click on the Notification / Conversation button, and wait for the menu to open
		button_to_click = self.selenium.find_element_by_xpath("html/body/div[1]/div[1]/div[2]/div[1]/div/button[1]").click()
		
		WebDriverWait(self.selenium, 30).until(lambda s: s.find_element_by_css_selector(".networkNotifDateHeader").is_displayed())
		
		#The test can then store the date displayed on the News tab in the variable news_date
		news_date = self.selenium.find_element_by_css_selector(".networkNotifDateHeader").text
		
		#Convert this string into a datetime object
		news_date_time = datetime.strptime(news_date, "%A, %d %B %Y")
		
		#Get the current datetime as a dateime object
		now_date_time = datetime.now()
		
		#The test can then compare date of news items to the current date, to ensure that news items do not display a date in the future. 
		assert (news_date_time <= now_date_time), "Test Fail: Date of news item occurs in the future"
	
		#Next the test wants to access the invite friends options, however there are multiple elements on the page which share the class 'buttonHolder' 
		#The first element on the page with the class 'buttonHolder is the 'Follow new Interests' button, the second is the 'Invite friends' button.
		#The test wants to click on the second button which uses the class 'buttonHolder'. 
		#By using find elements, instead of find element, selenium will return more than one element 
		#self.selenium.find_elements_by_css_selector(".buttonHolder")[0] will return the first element with class 'buttonHolder'
		#self.selenium.find_elements_by_css_selector(".buttonHolder")[1] will return the second element with class 'buttonHolder'
		
		#Click on the Invite friends button.
		button_to_click = self.selenium.find_elements_by_css_selector(".buttonHolder")[1].click()
		
		#Wait for Invite friends window to load, test waits for the the mail icon to be displayed before proceeding. 
		WebDriverWait(self.selenium, 30).until(lambda s: s.find_element_by_css_selector(".mailIcon").is_displayed())
		
		#Once the Invite friends options are displayed, identify the email text input box. 
		email_address_box = self.selenium.find_element_by_name('email')
		
		#The test needs to type in a unique email address which has not been sent an invite before.
		#This email address needs to be unique each time the test runs.
		#To meet both of these criteria, the test is going to enter a gmail alias to a valid gmail email account. 
		#Gmail supports email aliases by adding '+something' to the first part of address, email sent to aliases is received by the main gmail account.
		#Software generally can't tell the difference between a valid email address and a valid gmail alias and Pinterest is no exception to this.
		#To make a valid gmail alias for testing, the test is going to append the current epochtime to the current user's gmail address.
		#The alias would look something like: justaseleniumtest+1437131756@gmail.com
		
		epoch_time_now = calendar.timegm(time.gmtime())	
		email_alias = 'justaseleniumtest+'+ str(epoch_time_now) +'@gmail.com'		
		print(email_alias)
		
		email_address_box.send_keys(email_alias)
		email_address_box.send_keys(Keys.RETURN)
		
		#Wait until the invite confirmation message is displayed.
		WebDriverWait(self.selenium, 30).until(lambda s: s.find_element_by_css_selector(".inviteConfirm").is_displayed())
		
		#Scrape the text off the invite confirmation window and store it in variable invite_confirmation_text
		invite_confirmation_text = self.selenium.find_element_by_css_selector(".inviteConfirm").text
		self.assertEqual(invite_confirmation_text, 'Invitations sent!')
		
		#The 'Invitations sent!' message times out within 5 seconds and closes itself, wait for it to close.
		time.sleep(5)
		
		#Test sending a second invite to the same email address again
		email_address_box.send_keys(email_alias)
		email_address_box.send_keys(Keys.RETURN)
		
		#Wait until the message 'Ooops! You've already invited that person' is displayed.
		WebDriverWait(self.selenium, 30).until(lambda s: s.find_element_by_css_selector(".body").is_displayed())
		message_text = self.selenium.find_element_by_css_selector(".body").text
		
		#Assert the correct text is displayed when trying to invite the email address a second time.
		assert(message_text == "Oops! You've already invited that person."), "Unexpected text is displayed"
	
		
	
	def tearDown(self):
		#this is where all all the tidying up after the test is done. It's usually a good idea to close the browser window here.
		self.selenium.quit()
	

#The lines below are part of the unit test framework which tell Pytest to run the test 
if __name__=="__main__":
    unittest.main()
