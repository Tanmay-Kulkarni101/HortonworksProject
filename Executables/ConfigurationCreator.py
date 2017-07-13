'''
The aim of this tool is to help the user configure a file which tells the program how the data is structured, so that it can automatically run the test cases.
Note:The number of inputs must include the query string and the type of tab. 
Additionally, one must account for a tab and the points given for that tab as an input.
'''
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('')),'Resources'))
from properties import allowedInputs,allowedTypes,matchPoints,configurationFileAddress

#This list stores all the kind of input points possible
allowedInputPoints=[]

#We perform an enumeration so that the user can just input the number rather than inputting the whole string
matchInputs=dict(enumerate(allowedInputs))
matchTypes=dict(enumerate(allowedTypes))
#Generating a list of pointInputs
for anInput in allowedInputs:
	if 'STRING' in anInput:
		pass
	else:
		allowedInputPoints.append(matchPoints[anInput])
# print(allowedInputPoints)
if __name__=="__main__":
	wrtr=open(configurationFileAddress,'w')

	#Currently,we have only given support for text but this can also be extended for other formats such as JSON format
	print('Choose the type of input (for example text)')
	inputValue=input()
	cont=True
	if(inputValue.upper()=='TEXT'):
		wrtr.write('text\n')
		print('How many categories(type of inputs are there, Note: it should also include the points for a particular search result)')
		# Testing for the validity of the input
		while(cont):
			catNum=input()
			try:
				temp=int(catNum) #Checking if the input is a number
				cont=False
			except ValueError:
				print('Invalid Input,try again..')

		wrtr.write(catNum+'\n')
		print('Enter the delimiter other than a whitespace character,for values of the same type')
		cont=True
		while(cont):
			delim=input()
			if(delim.strip()!=''): #elimenating the whitspaces from the input, if the input is a whitespace, it will be converted to an empty string
				cont=False
			else:
				print('Invalid delimiter,try again')
		wrtr.write(delim+'\n')

		print('Enter the delimiter other than a whitespace character,for values of differenct type')
		cont=True
		while(cont):
			delim=input()
			if(delim.strip()!=''): #elimenating the whitspaces from the input, if the input is a whitespace, it will be converted to an empty string
				cont=False
			else:
				print('Invalid delimiter,try again')
		wrtr.write(delim+'\n')
		
		#Writing the different types of data into the configuration file
		while(temp>0):	
			print('Enter the categories in the order in which they appear in the input file')
			print('The input must belong to the following categories')
			for key,value in matchInputs.items():
				print("{0}. {1}".format(key,value))
			cont=True
			print('Enter the name of the Category:')
			while cont:
				cat=input()
				try:
					cat=matchInputs[int(cat)] # We make use of the dictionary here, if the individual makes use of a number to specify the choice
					cont=False
				except ValueError:
					if cat.upper() not in allowedInputs: #Checking if the text value matches one of the inputs
						print('Invalid Input,try again..')
					else:
						cont=False
				except KeyError:
					print('Invalid key value, the value must match the indices on the screen')
			try:
				if(cat.upper()==allowedInputs[0]): # We do not perform any action, if the input is a queryString
					pass
				else:
					pointVar=matchPoints[cat.upper()] # Here we map the input with the points alloted for the input
			except KeyError:
				print('Something strange happened,check the dictionary, some matches may be missing') #This may happen if we update the allowedInputs, but we do not account for the points given to it
			
			wrtr.write(cat.lower())	# the category is stored in lowercase
			
			
			# Here we enter the data type of the input, that is, if it is a string or an integer
			for key,value in matchTypes.items():
				print("{0}. {1}".format(key,value))
			cont=True
			# Checking the validity of the input of the user
			while(cont):
				typ=input()
				try:
					typ=matchTypes[int(typ)] # Checking if the user input value, matches with the dictionary that we created by enumeration
					cont=False
				except ValueError:
					if typ.upper() not in allowedTypes: # Checking the validity of the textual input
						print('Invalid Input,try again..')
					else:
						cont=False
				except KeyError:
					print('Invalid key value, the value must match the indices on the screen')

			wrtr.write(' , '+typ.lower()+'\n')

			if cat.upper()!=allowedInputs[0]:
				wrtr.write(pointVar.lower()+' ,'+'integer'+'\n') # Here we append the points given right after the particular type of input
				temp-=1
			cont=True
			temp-=1

	wrtr.close()
				





