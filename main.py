def getInput():
	return(input("Ask a question--/n"))

def requestMgr(input):
	print('debug')
	#send request to openAI API

def loop():
	requestMgr(getInput())
	print("Enter Z to quit. Enter X to prompt again.")
	uInput = input("")
	
	while True:
		try:
			uInput = str.casefold(input(""))
		except:
			print("Use letters only!")
			continue
	
		if uInput != 'Z' and uInput != 'X':
			print("Out of range error.")
			continue
		else:
			break

	if uInput == 'Z':
		exit(200,'OK')
	elif uInput == "X":
		loop()

loop()