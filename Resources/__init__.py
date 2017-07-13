##Defaults for the Configuration Helper
#allowedInputs is the different type of inputs the program can take and corrospond excactly to the tabs present within the program
allowedInputs=['QUERYSTRING','KNOWLEDGE BASE','CASES','CASE COMMENT','HORTONWORKS JIRA']
#The only types of input used are are characters and numbers, which are represented through INTEGER AND STRING respectively
allowedTypes=['INTEGER','STRING']
#This dictionary maps the tab and the points given for each tab.
matchPoints={'KNOWLEDGE BASE':'KB_POINTS','CASES':'CASE_POINTS','CASE COMMENT':'CASE_COMMENT_POINTS','HORTONWORKS JIRA':'HORTONWORKS_JIRA_POINTS'}