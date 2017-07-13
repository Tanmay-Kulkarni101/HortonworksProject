import fnmatch
import codeop


address1='ConfigurationHelper.py'
address2='DataValidator.py'
address3='SearchExecutor.py'
part1=open(address1,'r')
part2=open(address2,'r')
part3=open(address3,'r')
funclist1=[]
funclist2=[]
funclist3=[]
def checkValidity(line,fileWriter,count,startDebug):
	print('The count is:')
	print(count)
	if '#' in line:
		temp=line.strip()
		temp=temp.rsplit('#',1)[-1]
		temp=temp.strip()
		print(temp)
		try:
			codeop.compile_command(temp)
			print('********************************************************************************')
			print(temp)
			fileWriter.write(line.rsplit('#',1)[0]+temp+'\n')
			print('********************************************************************************')
		except SyntaxError:
			fileWriter.write(line)
	else:
		temp=line.strip()
		if "'''" in temp:
			count+=temp.count("'''")

		elif count>0 and count%2==0:
			if startDebug is False:
				print('******************************************************')
				print('Adding the debugging statement')
				temp=line.lstrip()
				indent=len(line)-len(temp)
				print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
				print('The indent is:')
				print(indent)
				i=0
				while(i<indent):
					fileWriter.write('\t')
					i+=1
				fileWriter.write('import pdb\n')
				i=0
				while(i<indent):
					fileWriter.write('\t')
					i+=1
				fileWriter.write('pdb.set_trace()\n')
				startDebug=True
		fileWriter.write(line)
	return count,startDebug

def toggleDebugging(index):
	fileReader=open(eval('address'+str(index)),'r')
	fileWriter=open(eval('address'+str(index))[:-3]+'Debug.py','w')
	startDebug=False
	count=0
	for line in fileReader:
		count,startDebug=checkValidity(line,fileWriter,count,startDebug)
	fileReader.close()
	fileWriter.close()

def enableFunctionDebugging(part,fnName):
	fileWriter=open(part[:-3]+'Function.py','w')
	fileReader=open(part,'r')
	enableDebug=False
	startDebug=False
	count=0
	indent=None
	print('The match is:')
	print(fnName)
	for line in fileReader:
		if enableDebug is True:
			temp=line.lstrip()
			print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
			print('It is:'+str(temp)+'[]')
			print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
			print('The indent of the function is:')
			print(len(line)-len(temp))
			print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
			if len(line)-len(temp)>=1 and temp!='':
				count,startDebug=checkValidity(line,fileWriter,count,startDebug)
			else:
				enableDebug=False
				fileWriter.write(line)
		else:
			print('line out of debug mode')
			print(line)
			fileWriter.write(line)
		if fnName in line:
			indent=line.rsplit('def',1)[0]+'\t'
			enableDebug=True
			print('The indent is:')
			print(len(indent))

	fileWriter.close()
	fileReader.close()
		

def populateFunctionlists(functionList,pythonScript):

	for line in pythonScript:
		if 'def' in line and ':' in line:
			functionList.append([aPart.strip() for aPart in line.split(' ')][len([aPart.strip() for aPart in line.split(' ')])-1][:-1])

for i in range(3):
	print('funclist%s'%(i+1))
	populateFunctionlists(eval('funclist%s'%(i+1)),eval('part%s'%(i+1)))
	print(eval('funclist%s'%(i+1)))
	exec('part%s.close()'%(i+1))

cont=True
funcFound=False
while(cont):
	print('Enter the function to be put into debugging mode, or enter the modular part to be put in debugging mode:')
	val=input()
	for i in range(3):
		match=fnmatch.filter(eval('funclist%s'%(i+1)),'*%s*'%val)
		if len(match)==1:
			print('The function is:')
			print(match)
			print('It is a part of')
			print('part%s'%(i+1))
			enableFunctionDebugging(eval('address%s'%(i+1)),match[0])
			funcFound=True
		elif len(match)>1:
			print('Too many matches,be more specific')
		elif val == 'part%s'%(i+1):
			print('Creating new debug file...')
			toggleDebugging(i+1)
			print(val)
			funcFound=True
	if(funcFound is False):
		print('No such function or part is present')
	print('Do you want to continue(y/n)')
	ext=input()
	if ext.upper()=='Y':
		pass
	else:
		cont=False








