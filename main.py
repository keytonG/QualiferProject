import os
import openai
import json
import time
from colorama import Fore, Back, Style
print(Fore.RED + Back.WHITE + "!! IF CODE STOPS UNEXPECTEDLY (FOR MORE THAN 1 MINUTE), RESTART !!")
print(Style.RESET_ALL)

print("Starting...")

openai.api_key = str(input("ENTER API KEY: "))


def clear():
	try:
		os.system('clear')
	except:
		os.system('cls')

class response: #final product of json digest
	def __init__(self,content,id): #call response.content for raw objects
		self.content = content,
		self.id = id

	def __iter__(self):
		yield {
			'content': self.content,
			'id': self.id
		}

	def getObject(self,obj): #returns filtered objects
				
		if obj == "content":
			table = dict.fromkeys(map(ord, ")(',"), None)
			return(str(self.content).translate(table))
		elif obj == 'id':
			return(str(self.id))
		else:
			quit("400; Bad Request (Malformed input)")


def digestJSON(input):
	print("Pre-processing response...")
	input = input.replace('\n'," ") #remove newline control characters
	x = json.loads(input) #translate json to python datatypes

	data = {
		'content': x['choices'][0]['text'], #Grabs text field from json
		'id':x['id'] #Grabs ID field from json
	}
	#return data in response class object
	return response(data['content'],data['id'])


y = []

def openAICall():
	#MAX $0.00896 PER DATASET; ASSUMES 64/64 TOKENS USED ON 7/7 PROMPTS
	prompts = [
		['retail store name, cannot be an existing company:',0],
		["product sold in a retail store and it's price:",1],
		["product sold in a retail store and it's price:",1],
		["product sold in a retail store and it's price:",1],
		["product sold in a retail store and it's price:",1],
		["product sold in a retail store and it's price:",1],
		["list of operating hours for a retail store:",2]
	] #last object in list designates prompt type
		#0 = store name, 1 = product & price, 2 = operating hours
	
	c,l = 0,7
	for i in prompts:
		try:
			c +=1
			print("Sending Request to server...")
			x = openai.Completion.create(
			model="text-davinci-003",
			prompt=i[0],
			temperature=0.83,
			max_tokens=64,
			top_p=1,
			frequency_penalty=0,
			presence_penalty=0
		)
		except openai.error.ServiceUnavailableError:
			quit("The server is currently unavailible. Try again soon.\n (Refer to errors.md with Code 0 for more information.)")
		except openai.error.RateLimitError:
			quit("Rate limited.\n (Refer to errors.md with Code 1 for more information.)")
		except openai.error.Timeout:
			quit("Server timed out.\n (Refer to errors.md with Code 2 for more information.)")
		except openai.error.AuthenticationError:
			quit("The server could not authenticate the supplied API key, or the key is invalid.\n (Refer to errors.md with Code 3 for more information.)")
		except:
			quit("An unknown error occured while contacting the server.\n (Refer to errors.md with Code 4 for more information.)")
			
		y.extend(digestJSON(str(x)))
		print(f"Complete! ({c}/{l})")
		
print("Contacting server...")
openAICall()


menuVariables = {
	"storeName":"",
	"products": [],
	"storeHours":None
}

print("Processing responses...")
c,l = 0,7
for i in y:
	if c != l:

		c+=1
		if c == 1:
			table = dict.fromkeys(map(ord, ")(,'",))
			table2 = dict.fromkeys(map(ord, '"'))
			i['content'] = str(i['content']).translate(table)
			i['content'] = i['content'].translate(table2)
			i['content'] = i['content'].replace('\\n','')
			menuVariables['storeName'] = (i['content']).capitalize()

		elif c > 1 and c <= 6:
			menuVariables['products'].extend(i['content'])

		elif c == 7:
			menuVariables['storeHours'] = i['content']
		print(f"Completed! {c}/{l}")


print("Initializing menu...")
def exitDiag():
	print("")
	print("-------------------------")
	print("Enter X to exit dialogue.")
	while True:
		try:
			xT = str.casefold(input(""))
			if xT != "x":
				continue
			elif xT == 'x':
				clear()
				break
		except TypeError:
			print('3')
			continue
		except:
			quit("400; Bad Request (Malformed input)")
			
def master(type):
	
	if type == 1:
		clear()
		for i in menuVariables['products']:
			print(i)
			

			
	elif type == 2:
		for i in menuVariables['storeHours']:
			print(i)
			
			
	elif type == 3:
		exit("Exitted!")
		
	exitDiag()
	
operationsTable = [
	{
		'name':'getProducts',
		'function':'master(1)',
		'spec':1
	},
	{
		'name':'getHours',
		'function':'master(2)',
		'spec':2
	},
	{
		'name':'quit',
		'function':'master(3)',
		'spec':3
	},
]

def printMenu():
	print(f"-- WELCOME TO {str.capitalize(str(menuVariables['storeName']))} --")
	print("----------------------------------------")
	print("")
	print("")
	print("Select a menu option:")
	print("1. View Products")
	print("2. View Store Hours")
	print("3. Exit")
	print("(Input the number of the option to select it.)")


def menu():
	while True:
		printMenu()
		try:
			uInput = int(input(""))
			print(uInput)
			if uInput > 4 or uInput < 1:
				clear()
				print("Please select only 1 menu option. Returning to menu in 10 seconds...")
				time.sleep(10)
				clear()
				continue
			break
		except:
			clear()
			print("Enter the option's list number to select it. Returning to menu in 10 seconds...")
			time.sleep(10)
			clear()
			continue

	for i in operationsTable:
		if i['spec'] == uInput:
			clear()
			exec(i['function'])
		else:
			continue

print("Menu ready!")
print("Starting...")
time.sleep(3)
clear()

while True:
	menu()