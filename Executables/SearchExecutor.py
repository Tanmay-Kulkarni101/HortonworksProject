'''
The aim of this program is to send the user defined search query to the smart search and then analyze the results that it has ouput with the help of webscrapping using selenium webdriver
Note: This program uses python 3 and needs the geckodrver along with firefox installed. If we wish other browser compatability we need to install the driver for chrome and utilize the function calls for chrome.

Furthermore,this program requires duplicateContiuned to run, inorder to validate the configuration and input files. 

___________________________________________________________________________________________________________________________________________________________________________
Summary:
This program first initializes an instance of firefox, after which, it navigates to the smartsearch page. After this, we search for the search box in which we input the 
search query. Then we detect the number of main tabs. We then loop through these main tabs and find the sub tabs for each. After this, we loop through each subtab and 
extract the results on each page, which we store in the form of a tree, which is created with the help of dictionaries and lists. We then find the required tabs whose data 
is to be examined through the configuration file. We then extract that data and obtain the points through the mapping created in duplicate continued.
____________________________________________________________________________________________________________________________________________________________________________
'''
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('')),'Resources'))
from properties import address,login,aCookie,outputFileAddress,waitingTime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import sys
import requests
import time
from DataValidator import tempList,queryList,testTypes,pointValueMap
from ConfigurationCreator import matchPoints
import json
import datetime
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',filename=os.path.join(os.path.dirname(os.path.realpath('')),'ProgramLogs/RunLog.log'),level=logging.DEBUG)
# The list containing the search results of each search query
resultSummary=[]
finalOuput={}
# string1='tez view No records available'
# string2='Ambari not showing "Perform Upgrade"'
# To manully run fixed test cases

def start():
	'''The role of this function is to initilize the webdriver to the required page and return the initialized driver and the position of the search string'''
	# Initialize the firefox webdrive. Note: geckodriver must be installed
	logging.info('Initializing the web driver')
	driver=webdriver.Firefox()
	logging.warning('Using a cookie for login,please find a more robust method in the future.')
	logging.info('Going to the login page')
	driver.get(login)
	logging.warning('Applying Cookie')
	driver.add_cookie(aCookie)
	logging.warning('Navingating to the new Smart Search Page')
	driver.get(address)
	# Navigating to the required address
	return (driver)

def sendQuery(queryString):
	'''This function searches for the input element and then sends the search keys to it '''
	try:
		# Here we either obtain an input element or receive a timeout exception after a period of 5 seconds. The reason for setting a wait is so that the webpage can handle all asyndhonus calls, after whichwe extract the results
		inp=WebDriverWait(driver,waitingTime).until(EC.presence_of_element_located((By.XPATH,"//input[@type='text']")))
	except TimeoutException:
		print('Element not found. There was no input on the page')
	# Clears the input field
	inp.clear()
	# Send the requisite search query
	inp.send_keys(queryString)
	# Submits the search query to the web page
	inp.submit()

def tabsPresent(outerElement):
	'''This program searches for the presence of tabs within an WebElement passed to it'''
	try:
		# Here we try to find the unordered list that has the role attribute of tablist
		searchNav=outerElement.find_element_by_xpath('.//ul[@role="tablist"]')
		# we then store all the tabs in a list in allTabs
		allTabs=searchNav.find_elements_by_tag_name('li')
		return allTabs
	except NoSuchElementException:
		return None

def subData(typeDiv):
	'''The role of this function is to pull out the data from the subtabs and store in the form of {subtab:[data]} or {'DEFAULT':[data]}'''
	subTabs=tabsPresent(typeDiv)
	collection={}
	if (subTabs is None):
		# print('No sub tabs are present')
		## Action if tab directly contains the data
		try:
			## Here we search for a table element within which we identify all the hyperlinks that we store in the list
			logging.info('No sub tabs present.')
			logging.info('The data within the main tab')
			subTab={'DEFAULT':[]}
			table=typeDiv.find_element_by_xpath('.//table')
			elems=table.find_elements_by_xpath('.//a')
			if elems!=[]:
				for elem in elems:
					# print('...............................................')
					# print(elem.text)
					subTab['DEFAULT'].append(elem.text)
					logging.info(elem.text)
					# print('...............................................')
				collection.update(subTab)
				return collection
			else:
				## If no results are found
				# print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
				# print('There is no content on page')
				# print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
				logging.info('No content on page')
				collection.update(subTab)
				return collection
		except NoSuchElementException:
			logging.critical('There is no table present, the page formatting may have changed.')
			print('No results found')
	else:
		for tab in subTabs:
			subTab={}
			subtext=''
			## Navingating through each sub tab
			# print('getting data from')
			# print(tab.text)
			subtext=tab.text.rsplit(' ',1)[0].upper()
			logging.info('The sub tab is %s',subtext)
			subTab={subtext:[]}
			link=tab.find_element_by_xpath('.//a')
			## Verifying that we have the corrent link element
			# print('The link')
			# print(link)
			link.click()
			## Obtaining the data from each subtab
			subTab[subtext]=(getData(typeDiv))
			collection.update(subTab)
		return collection

def getData(contentDiv):
	'''Here we obtain the results stored within each subtab'''
	logging.info('The data within the subtab')
	subresult=[]
	WebDriverWait(contentDiv,waitingTime).until(EC.presence_of_element_located((By.XPATH,".//div[contains(@class,'active in') or contains(@class,'in active')]")))
	subDiv=contentDiv.find_elements_by_xpath('.//div[contains(@class,"active in") or contains(@class,"in active")]')
	# print('The sub div is:')
	# print(subDiv)
	# print('The id of the subdiv is:')
	# print(subDiv[0].get_attribute('id'))
	## Checking the correctness of the div element extracted
	for div in subDiv:
		if(div.is_displayed()):
			# Finding the table containing the data
			table=div.find_element_by_xpath('.//table')
			# print('The table in the sub div is')
			# print(table)
			## Checking the presence of the table
			## Here we identigy all the rows within each table ager which we identify a heading type that we store into the subresult
			headingsFound=False
			try:
				tableRows=table.find_elements_by_xpath('.//tr')
				for tableRow in tableRows:
					tableData=tableRow.find_element_by_xpath('.//td')
					paragraphs=tableData.find_elements_by_xpath('.//p')
					headingTypes=['h1','h2','h3','h4','h5']
					for headingType in headingTypes:
						# print('The type of heading is:')
						# print('.//%s'%headingType)
						##Verifying the type of heading
						try:
							heading=paragraphs[0].find_element_by_xpath('.//%s'%headingType)
							# print('the heading within the table row is:')
							# print(heading)
							part=heading.find_element_by_xpath('.//a')
							headingsFound=True
							# print('-------------------------------------------------------------0')
							# print(part.text)
							subresult.append(part.text)
							logging.info('part.text')
							# print('--------------------------------------------------------------1')
						except NoSuchElementException:
							pass
					# print('Finished one type')
				if(headingsFound is False):
					## If no results are found on page, no headings will be found
					# print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
					# print('There is no content on page')
					# print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
					logging.info('No results present')
					return []
			except NoSuchElementException:
				pass
	# print('*** **** ******* **** ******* **** ******* **** ******* **** ******* **** ******* **** ******* **** ******* **** ******* **** ****')			
	# print('The value stored in subresult is:')	
	# print(subresult)	
	# print('*** **** ******* **** ******* **** ******* **** ******* **** ******* **** ******* **** ******* **** ******* **** ******* **** ****')	
	return subresult

def extractData():
	'''This function searches for the main tabs on the page, after which it navigates to each tab.Then it searches for the div holding content for each tab. 
		We then search for the first active div that is displayed, which we send to subData in order to obtain the data within the subtabs
	'''
	resultCollection={'data':[]}
	try:
		## Searching for the first unordered list on the page having the role tablist. And giving a timeout error if we are unable to find this element in 5 seconds
		logging.info('Searching for the main tabs.')
		WebDriverWait(driver,waitingTime).until(EC.presence_of_element_located((By.XPATH,"//ul[@role='tablist']")))
	except TimeoutException:
		print('Element not found. No tabs were present on the page')
	mainTabs=tabsPresent(driver)
	if (mainTabs is None ):
		logging.critical('No main tabs are present.')
		print('No tabs were found')
		sys.exit('The program crashed')
	## Delay for the initial data to load 
	time.sleep(5)
	for tab in mainTabs:
		if (tab.is_displayed()):
			# print('The main tab is ******************************')
			# print(tab.text)
			# print('***********************************************')
			## Check if each main tab is accessed
			## Navigating to each link
			link=tab.find_element_by_xpath('.//a')
			logging.info('The main tab is %s',link.text)
			link.click()
			## Here we remove the number of results obtained part within each tab
			# print('+-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-+')
			# print('The first part is:')
			mainTab=tab.text.rsplit(' ',1)[0].upper()
			# print(mainTab)
			resultCollection['data'].append({mainTab:[]})
			# print('+-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-++-+-+')
			## Delay for the content to load
			time.sleep(10)
			try:
				masterDiv=driver.find_elements_by_xpath('//div[@class="tab-content"]')
				# print(masterDiv[0].get_attribute('style'))
				## Checking if we have the correct div
				## Finding the current active div
				divs=masterDiv[0].find_elements_by_xpath('.//div[contains(@class,"active in") or contains(@class,"in active")]')
				for div in divs:
					if div.is_displayed():
						mainDiv=div
						## Checking if we got the correct div containing the data of the main tab
						# print(div.get_attribute('id'))
						obtainedData=subData(mainDiv)
						if obtainedData is None:
							pass
						else:
							for key,value in obtainedData.items():
								## Appending the mainTab Values
								resultCollection['data'][len(resultCollection['data'])-1][mainTab].append({key:[]}) 
								# print('.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,..')
								# print(resultCollection)
								# print('[][][][][][][]{}{}{}{}{}{}{}[][][][][][][][][][][][][][][][][][][][][][]')
								## Appending the dictionary to the tree
								resultCollection['data'][len(resultCollection['data'])-1][mainTab][len(resultCollection['data'][len(resultCollection['data'])-1][mainTab])-1][key]=(value)
								# print('[][][][][][][]{}{}{}{}{}{}{}[][][][][][][][][][][][][][][][][][][][][][]')
			except TimeoutException:
				print('Element not found, the content <div> was not displayed')
			except NoSuchElementException:
				print('Unable to find the active <div> containing the data')
	return resultCollection


def getSubTabValues(summary,mainTab):
	'''This function returns a part of the tree of a main tab'''
	valueOf=lambda key,inputData:[subVal[key] for subVal in inputData if key in subVal]
	# print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
	temp=valueOf(mainTab,summary['data'])
	# print(temp[0])
	# print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
	return temp[0]
	
def calculateScore(listOfResults,resultMap):
	'''This function finds the points through the mapping passed to it and also records the change in position'''
	foundValues={}
	points=0
	isInt=isinstance(list(resultMap.keys())[0],int)
	# print(isInt)
	if(isInt):
		for aValue in listOfResults:
			try:
				intForm=int(aValue)
				# print('The integer form of the value is:')
				# print(intForm)
				try:
					points+=resultMap[intForm]
					foundValues.update({list(resultMap.keys()).index(intForm):listOfResults.index(aValue)})
				except KeyError:
					pass
			except ValueError:
				print('The configuration file specified an integer, however the results on the page seem to be a string')
	else:
		for aValue in listOfResults:
			try:
				points+=resultMap[aValue]
				foundValues.update({list(resultMap.keys()).index(aValue):listOfResults.index(aValue)})
			except KeyError:
				pass
	print('The total points:')
	print(points)
	print('The positions of the results obtained:')
	print(foundValues)
	return points,foundValues

def searchByLayer(summary,query):
	'''This function parses through the tree and finds the tabs relevant to the user and then sends it to calculateScore to find the rating'''
	valOf=lambda key,inputData:[subVal for subVal in inputData if key in subVal]
	# testTypes=['KNOWLEDGE BASE']
	# matchPoints={'KNOWLEDGE BASE':'KB_POINTS','CASE':'CASE_POINTS','CASE COMMENT':'CASE_COMMENT_POINTS'}
	# pointValueMap=[{'KB_POINTS': {4720: 1, 3154: 1, 5631: 3, 5069: 1, 5834: 1}}]
	allResultList=[]
	subTabs=[]
	mainTabList=[]
	subTabList=[]
	## Taking the main tab from the keys within the dictionary and then converting it into CAPITALS
	mainTabs=list(map(lambda y:y.upper(),list(map(lambda x:list(x.keys())[0],summary['data']))))
	## Verifying the value of main tabs
	# print('The main tabs are:')
	# print(mainTabs)
	## Checking if the main tabs match what the user needs
	mainTabResults=list(set(mainTabs)&set(testTypes))
	## Extracting the part of the tree which is relevant
	for mainTab in mainTabResults:
		mainTabList+=valOf(mainTab,summary['data'])
	# print('The mainTab List is:')
	# print(mainTabList)
	# print('The mainTab Results are:')
	# print (mainTabResults)
	for mainTab in list(set(mainTabs)-set(mainTabResults)):
		## Extracting the subtab values by first obtaining the list of subtabs, from which the keys are extracted and strored in CAPITALS
		subTabs+=list(map(lambda y:y.upper(),list(map(lambda x:list(x.keys())[0],getSubTabValues(summary,mainTab)))))
		## Individully storing the parts of the tree which is relevant to the user
		subTabList+=getSubTabValues(summary,mainTab)
	subTabResults=list(set(subTabs)&set(testTypes))
	allTabResults=list(set(subTabResults)|set(mainTabResults))
	logging.info('The relevant tabs are:')
	logging.info(allTabResults)
	## Verifying the validity of the results obtained
	# print('All Tab Results:')
	# print(allTabResults)
	# print('The subTabList is')
	# print(subTabList)
	mapping={}
	for aResult in allTabResults:
		if aResult in mainTabs:
			## Finding the relevant part of the tree
			print('Obtaining the score for.... %s'%aResult)
			dataOp=valOf(aResult,mainTabList)
			dataOp=dataOp[0]
			temp=valOf(matchPoints[aResult],pointValueMap)
			temp=temp[0]
			temp=temp[matchPoints[aResult]]
			## Checking if we correcly obtained a point mapping and the list of results
			# print('The mapping of points')
			# print(temp)
			# print('The requisite tablist')
			# print(dataOp[aResult][0]['DEFAULT'])
			mapping.update({aResult:calculateScore(dataOp[aResult][0]['DEFAULT'][:min(len(dataOp[aResult][0]['DEFAULT']),len(temp.keys()))],temp)})
		else:
			print('Obtaining the score for.... %s'%aResult)
			dataOp=valOf(aResult,subTabList)
			dataOp=dataOp[0]
			temp=valOf(matchPoints[aResult],pointValueMap)
			temp=temp[0]
			temp=temp[matchPoints[aResult]]
			## Checking if we correcly obtained a point mapping and the list of results
			# print('The mapping of points')
			# print(temp)
			# print('The requisite tablist')
			# print(dataOp)
			mapping.update({aResult:calculateScore(dataOp[aResult][:min(len(dataOp[aResult]),len(temp.keys()))],temp)})
		finalOuput[query]=mapping

# Program starts here __main()__
logging.info('Running the Search Executor')
driver=start()
for query in queryList:
	logging.info('Running the query %s',query.strip())
	print('Obtaining the data for')
	print(query)
	# To find out if the postion of the search query mathces with that of the configuration file

	# Sending the search query to the webpage.
	sendQuery(query)
	# Adding the results collected from the webpage into the result summary
	resultSummary+=[{query:extractData()}]

# print(resultSummary)
print(json.dumps(resultSummary,indent=4))
for query in queryList:
	logging.info('Finding points:')
	print('90909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909')
	print(json.dumps(resultSummary[queryList.index(query)][query],indent=4))
	finalOuput.update({query:None})
	searchByLayer(resultSummary[queryList.index(query)][query],query)
	print('90909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909')

print(json.dumps(finalOuput,indent=4))
outFile=open(outputFileAddress,'a')
outFile.write('=========================Time(YYYY/MM/DD):(Hours|Min)-({0}/{1}/{2}):({3}|{4})=====================================================================================\n'.format(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,datetime.datetime.now().hour,datetime.datetime.now().minute))
outFile.write(json.dumps(finalOuput,indent=4))
outFile.write('\n')
outFile.write('<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n')
outFile.close()
time.sleep(100)
driver.close()
