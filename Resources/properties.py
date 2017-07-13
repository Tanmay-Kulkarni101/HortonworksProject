##General Properties
#Location of the input file
import os
#Searching for the parent folder for the resources folder and extracting the required files
inputFileAddress=os.path.join(os.path.dirname(os.path.realpath('')),'Resources/input.txt')
configurationFileAddress=os.path.join(os.path.dirname(os.path.realpath('')),'Resources/config.txt')
outputFileAddress=os.path.join(os.path.dirname(os.path.realpath('')),'Resources/results.txt')
##Defaults for the Configuration Helper
#allowedInputs is the different type of inputs the program can take and corrospond excactly to the tabs present within the program
allowedInputs=['QUERYSTRING','KNOWLEDGE BASE','CASES','CASE COMMENT','HORTONWORKS JIRA']
#The only types of input used are are characters and numbers, which are represented through INTEGER AND STRING respectively
allowedTypes=['INTEGER','STRING']
#This dictionary maps the tab and the points given for each tab.
matchPoints={'KNOWLEDGE BASE':'KB_POINTS','CASES':'CASE_POINTS','CASE COMMENT':'CASE_COMMENT_POINTS','HORTONWORKS JIRA':'HORTONWORKS_JIRA_POINTS'}
##Defaults for Data Validator
##Defaults for SearchExcecutor
# Addresses to be used for initialization
login='https://datalake.smartsense.hortonworks.com'
address='https://datalake.smartsense.hortonworks.com/smartsearch/'
localAddress='http://172.26.70.154:8080/smartsearch/'
alternateAddress='http://172.26.98.14:8080/smartsearch/'
#This is a JWT Token having a validity of one year and is added as a cookie to gain login access.
aCookie={'name': 'jwt',
	 'value' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJleHAiOjE0OTk5NTEyNDcsImlhdCI6MTQ5OTk0MTI0NywidXNlciI6InRrdWxrYXJuaSIsImdyb3VwcyI6ImNvbmZsdWVuY2UtdXNlcnMsc2VjdXJpdHkuaGlwY2hhdC11c2VycyxpbnRlcm5zLWFwYWMtaW5AaG9ydG9ud29ya3MuY29tLFNlY3VyaXR5LjAwMDAzMSxQcm9kdWN0IE9yZyIsInN1cHBvcnRVc2VyIjoidHJ1ZSJ9.kzN3NOeIKmJq-aZgu21XO1JIYczcXcbFoeeQr7WISF1NS8jUmWE_YKD1x8hXwd9XyQhydq5CCMdFThLjry-fJg',
	 'path' : '/'}
#Default wait setting for the content to load on to the webpage
waitingTime=5