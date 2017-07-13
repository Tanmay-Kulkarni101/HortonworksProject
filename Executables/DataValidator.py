'''
The aim of this program is to check the validity of the configuration file and the validity of the input file that will be used for checking the validity of the search results
Note: Make sure that the encoding of the input text files is ascii, so as to avoid any encoding isseus. If using special characters is absoultely necessary change the encoding options to tha required format.
In the open function
Note: This program has been designed to handle text files only, additionally more functionality can be added by handling more types like JSON files
'''
from ConfigurationCreator import allowedTypes,allowedInputs,allowedInputPoints
from collections import OrderedDict
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('')),'Resources'))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('')),'ProgramLogs'))
from properties import configurationFileAddress,inputFileAddress
import logging
# Globally decalred variables which store essential data in a structured manner
# The tabs from which the data is to be tested
testTypes=[]
# A mapping from the Points given for an input and the points given, which is obtained from the input file. The points are stored in a list
pointValueMap=[]

queryList=[]
class dataTemplate(object):
	'''This class defines a template for the way in which data is stored into the file'''
	def __init__(self,name,typ):
		self.catName=name
		self.catType=typ

def checkTemplate(template):
	'''This function validates the format of the template, by checking if the type (integer,string) belongs to a predefined set of allowed inputs'''
	for dataItem in template:
		# print('*************The type is*****************')
		# print(dataItem.catType.upper())
		# print('*******************************************')
		# print('-------------Checking the validity-----------')
		# print(dataItem.catType.upper() in allowedTypes)
		# for t in allowedTypes:
			# print('An allowed type is:')
			# print(t)
			# For debugging the configuration file
		if dataItem.catType.upper() not in allowedTypes:
			logging.critical('The type is not valid, stopping execution.')
			raise TypeError('Invalid data type please reset the configuration file') # if type does not match,we raise a type error
		if dataItem.catName.upper() not in allowedInputs+allowedInputPoints:
			logging.critical('The category used is invalid, stopping execution.')
			raise TypeError('The data entered is invalid, please check the cofiguration file and the predefined values within default.py') # if there are invalid inputs raise a type error

	return None

def fileRead(template,sameCatDelim,diffCatDelim,inputFile):
	'''This fuction checks the validity of the data that has been input into the text file'''
	for line in inputFile:
		logging.info('reading the line %s',line.strip())
		listOfSizes=[]
		prevSize=-1
		lineData=[parts.strip() for parts in line.split(diffCatDelim)] # We generate a list of all the values in the line separated by a delimiter, the parts are then cleared of whitespaces and is stored into line data
		# print('***************************************************************************************************************************************')
		# print('After separating the categories')
		# print(lineData)
		# print('***************************************************************************************************************************************')
		for anInputCategory in lineData:
			size=0
			valueMap=OrderedDict()
			lineDataParts=[vals.strip() for vals in anInputCategory.split(sameCatDelim)]
			# print('___________________________________________________________________________________________________________________________________')
			# print('After dividing the individual values:')
			# print(lineDataParts)
			# print('___________________________________________________________________________________________________________________________________')
			for lineDataPart in lineDataParts:
				size+=1
				# print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
				# print('The category being tested is %s'%tempList[lineData.index(anInputCategory)].catName.upper())
				# print('The type is %s'%tempList[lineData.index(anInputCategory)].catType.upper())
				# print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
				## Debugging issues related to the reading and correct splitting of files.
				# Checking if the types match with the specification in the configuration file
				if tempList[lineData.index(anInputCategory)].catType.upper()=='STRING':
					if 'STRING' in tempList[lineData.index(anInputCategory)].catName.upper():
						logging.info('Adding the query:%s',lineDataPart)
						queryList.append(lineDataPart)
					if not (isinstance(lineDataPart,str)):
						logging.critical('The part is not a query string')
						raise TypeError('The program expected a string in this position, however it received a %s'%type(lineDataPart))
				elif tempList[lineData.index(anInputCategory)].catType.upper()=='INTEGER':
					try:
						# print('Converting to INTEGER value')
						lineDataPart=int(lineDataPart)
						# print(lineDataPart)
						# print(tempList[lineData.index(anInputCategory)].catName.upper())
						## Mapping for the search result values and the points alloted to each of them.
						if 'POINTS' in tempList[lineData.index(anInputCategory)].catName.upper():
							# print('Comparing sizes')
							# print('The size is:')
							# print(size)
							# print('The prevsize was')
							# print(prevSize)
							# print(size>prevSize)
							## Debugging the mappings
							if size>prevSize:
								raise TypeError('You have more points than values to be mapped')
							else:
								print('Updating the value map')
								# Going to the results whose values are to be mapped.
								tempParts=[val.strip() for val in lineData[lineData.index(anInputCategory)-1].split(sameCatDelim)]
								# print('The temporary data is:')
								# print(tempParts)
								# print('The index is:')
								# print(size-1)
								# print('At the mapping position')
								# print(tempParts[size-1])
								## Debugging problems related to mapping.
								## Making sure that numbers are stored as integers.
								try:
									valueMap.update({int(tempParts[size-1]):lineDataPart})
								except ValueError:
									valueMap.update({tempParts[size-1]:lineDataPart})
								print(type(valueMap))
								print(valueMap)
					except ValueError:
						logging.critical('The data is not of integer type')
						raise TypeError('The program expected an integer in this position, however it received a %s'%type(lineDataPart))
			# print('The size is:')
			# print(size)
			# print('The prevsize was')
			# print(prevSize)
			## Making sure that the sizes are stored correctly so that each value has a unique mapping.
			prevSize=size
			## Checking if the values to be mapped and the scores are equal in number.
			if 'POINTS' in tempList[lineData.index(anInputCategory)].catType.upper():
				if size<prevSize:
					raise TypeError('You have too many values as compared to the points to be mapped')
			prevSize=size
			# listOfSizes.append(size)
			global pointValueMap
			# print('The valueMap is')
			# print(valueMap)
			## Making sure mappings are correct
			if valueMap!={}:
				pointValueMap.append({tempList[lineData.index(anInputCategory)].catName.upper():valueMap})
		# print('The list of sizes:')
		# print(listOfSizes)
		## Debugging the mapping issues.

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',filename=os.path.join(os.path.dirname(os.path.realpath('')),'ProgramLogs/RunLog.log'),level=logging.DEBUG)
logging.info('Start of the Data Validator Application')
redrCnfg=open(configurationFileAddress,'r')
redrInp=open(inputFileAddress,'r',encoding='ascii')
logging.info('Files opened successfully')
tempList=[] # The list of different inputs, obtained from the configuration file
delim=' '


print('Reading Confing Files.......')
fileType=redrCnfg.readline()
fileType=fileType.strip()
print(fileType)

if(fileType.upper()=='TEXT'):
	logging.info('Reading text based input file')
	numCat=redrCnfg.readline().strip()
	sameCatDelim=redrCnfg.readline().strip()
	diffCatDelim=redrCnfg.readline().strip()
	for line in redrCnfg:
		name,typ=line.split(',')
		# print('The category name is:')
		# print(name)
		# print('The type of the category is:')
		# print(typ)
		## To debug the input from the configuration file
		logging.info('Creating template')
		tempList.append(dataTemplate(name.strip(),typ.strip())) # Appending the category of input to the list
		if 'POINTS' not in name.upper() and 'QUERY' not in name.upper():
			testTypes.append(name.strip().upper())
else:
	print('something weird happened')


try:
	logging.info('Checking the validity of the configuration file.')
	checkTemplate(tempList) ## Checking the validity of the configuration file
	logging.info('The configuration file is valid.')
except TypeError :
	import sys
	sys.exit('Stopping execution...incorrect configuration file')

try:
	logging.info('Reading the input file.')
	fileRead(tempList,sameCatDelim,diffCatDelim,redrInp) # Checking the validity of the data of the input file
	logging.info('Reading Complete.')
except TypeError:
	import sys
	sys.exit('Stopping execution...data does not match the configuration file')
# print('The data extracted from input')
# print(dataList[0].unit)
print('_/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\_')
print(testTypes)
print('_/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\__/\_')
## Debugging the data extracted and the types given by the user

print('0000001010101010010101010101010010101010101010101000000000000000000000000000101010101010000000101010100000000')
print('The point value map is:')
print(pointValueMap)
print('0000001010101010010101010101010010101010101010101000000000000000000000000000101010101010000000101010100000000')
## Checking the validity of the mapping of the point values and the results
print(queryList)