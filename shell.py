"""
Appart from containing the class object of shell
this file also contains some miscellaneous tools, such as syntax parsing
"""



import os
from datetime import datetime
import json


class shell:
	def __init__(self, path=os.getcwd(), prompt=">", addons={}, lastCommand=None):

		self._prompt = prompt
		self.userinput = []
		self.addons = addons
		self.lastCommand = lastCommand
		self.variables = {}

		# This dictionary will contain keys (command names) that will refer to arrays of strings (orders)
		self.customCommands = {}
		os.chdir(path)

		if not callable(lastCommand) and lastCommand != None:
			raise Exception(f"The last command is not callable, object type: {type(lastCommand)}")



	def changePrompt(self, newPrompt):
		"""
		Changes the prompt of the console\n
		It also has some keys such as:\n
		$D -> current path\n
		$T -> current time\n
		"""
		self._prompt = newPrompt


	def askForInput(self):
		"""
		Updates the userinput property
		"""

		prompt = self._prompt

		if "$D" in prompt:
			prompt = prompt.replace("$D", os.getcwd())


		if "$T" in prompt:
			prompt = prompt.replace("$T", f"{datetime.today().hour}:{datetime.today().minute}:{datetime.today().second}")

		userinput = syntax.parseString(input(prompt))
		self.userinput = userinput

	def loopShell(self):
		"""
		Loops the ask for input
		"""

		while True:
			self.askForInput()
			self.executeInput()

	def executeInput(self, newInput=None):
		if newInput != None:
			self.userinput = syntax.parseString(newInput)


		if len(self.userinput) == 0:
			return 0

		else:
			result = []

			# Variables
			for par in self.userinput:			
				x = False # This indicates if the parser is in a variable calling or not
				foo = "" # Stores temporarily the string
				par += " " # The parameter that is going to be parsed
				fooVar = "" # The temporaral variable for the variable name in case that there is a varible call

				for char in par:
					
					if char == "$":
						# If the start of the variable has been already declarated
						if x:
							if not fooVar in self.variables:
								foo += "NULL"
 
							else:
								foo += str(self.variables[fooVar]) 


							x = False
							fooVar = ""
							continue


						else:
							x = True
							continue

					if x:
						fooVar += char
						continue

					else:
						foo += char

				result.append(foo.strip())

			self.userinput = result

			command = self.userinput[0]
			args = []

			# Arguments available
			if len(self.userinput) > 1:
				args = self.userinput[1:]

			# Empty input // This should happen in the terminal, but in scripts its possible to happen
			if command == "":
				return


			# builtin commands
			if command == "changedir" or command == "cd":
				self.changedir(args)
				return

			if command == "create":
				self.createRemoveElement(1, args)
				return

			if command == "remove":
				self.createRemoveElement(2, args)
				return

			if command == "listdir" or command == "ls":
				self.listdir(args)
				return
			
			if command == "set":
				self.setVariable(args)
				return

			if command == "import":
				self.importVariables(args)
				return

			if command == "export":
				self.exportVariables(args)
				return

			else:
				#Check if the command is in the addon dictionary
				
				if command in self.addons:
					self.addons[command](os.getcwd(), args)
					return

				else:
					args.insert(0, command)
					try:
						self.lastCommand(os.getcwd(), args)

					except TypeError:
						raise Exception("This function looks like it's not set for being called as the shell does.\n"+
							"There are two arguments parsed into the 'lastCommand' function, current path, and arguments.")

					except Exception as error:
						print(f"An error has occurred while trying to execute the 'lastCommand' function:\n{error}\nError type: {type(error)}")


	# Commands ----------------------------------------------------------

	def changedir(self, args):
		currentPath = os.getcwd()
		if len(args) == 0:
			print(currentPath)
			return

		else:
			try:
				os.chdir(args[0])
			except FileNotFoundError:
				print(f"Path doesn't exist: {args[0]}")
				return

	def createRemoveElement(self, typeOfAction, args):

		if not "--dir" in args and not "--file" in args:
			print(f"The type of the element wasn't specified. (--dir / --file)")
			return

		# Create element
		if typeOfAction == 1:

			# File
			if "--file" in args:
				try:
					del args[args.index("--file")]
					target = open(args[0], "w")
					target.write("")
					print(f"File created as: {args[0]}")

				except IndexError:
					print(f"Element name not specified")

				return

			# Directory
			if "--dir" in args:
				try:
					del args[args.index("--dir")]
					os.mkdir(args[0])
					print(f"Directory created as: {args[0]}")

				except FileExistsError:
					print(graphics.createErrorLog("The element already exists."))

				except PermissionError:
					print(graphics.createErrorLog("Cannot create an element in this directory, permission denied."))

				except IndexError:
					print(f"Element name not specified")


				return

		# Delete element
		if typeOfAction == 2:

			# File
			if "--file" in args:
				try:
					del args[args.index("--file")]
					os.remove(args[0])
					print(f"File removed: {args[0]}")

				except FileNotFoundError:
					print(graphics.createErrorLog(f"File not found: {args[0]}"))

				except PermissionError:
					print(graphics.createErrorLog(f"Cannot delete the file, permission denied"))

				except IndexError:
					print(graphics.createErrorLog(f"Element name not specified"))

				return

			if "--dir" in args:
				try:
					del args[args.index("--dir")]
					os.rmdir(args[0])
					print(f"Directory removed: {args[0]}")

				except FileNotFoundError:
					print(graphics.createErrorLog(f"Directory not found: {args[0]}"))

				except PermissionError:
					print(graphics.createErrorLog(f"Cannot delete the folder, permission denied"))

				except IndexError:
					print(f"Element name not specified")

				return


		else:
			raise Exception("The type of action specified doesn't fit to the availables.")



	def setVariable(self, args):
		"""
		Shows all the available variables, or sets a new one
		"""
		settings = []

		for index, argument in enumerate(args):
			if argument.startswith("--"):
				settings.append(argument)
				del args[index]

		if len(args) == 0:
			if len(self.variables) == 0:
				print("There are no variables set.")
				return

			else:
				print(graphics.createTitle("AVAILABLE VARIABLES:"))
				for variable in self.variables:
					print(f"\t[{variable}]: {self.variables[variable]}")

		else:
			varName = args[0]
			value = ""

			if len(args) >= 2:
				value = args[1]

			if "--input" in settings:
				newPrompt = ""
				

				# A prompt can be set by putting a second argument (not considering the options)
				if len(args) == 2:
					newPrompt = args[1]

				value = input(newPrompt)
				
			if "--delete" in settings:
				if len(args) == 1:
					varName = args[0]

					if not varName in self.variables:
						raise Exception(f"The specified variable couldn't be found: '{varName}'")

					else:
						del self.variables[varName]
						return

				else:
					raise Exception(f"Too many / few arguments, number of arguments: '{len(args)}'")

			try:
				value = int(value)
			except ValueError:
				pass

			self.variables[varName] = value


	def importVariables(self, pars):
		if len(pars) == 0:
			raise Exception("You didn't specify the path of the file to import.")

		else:
			if "--help" in pars:
				print("Imports variables from a file.")
				print("\tmove $file$")
				return

			else:
				content = json.loads(open(pars[0], "r").read())
				for key in content:
					if type(content[key]) != str and type(content[key]) != int:
						raise Exception(f"Invalid variable type: '{type(content[key])}'")
					else:
						self.variables[key] = content[key]


	def exportVariables(self, pars):
		if len(pars) == 0:
			raise Exception("Name of output file not specified.")

		if pars[0] == "--help":
			print("Exports the variables set in the current session into a file.")
			print("Usage:")
			print("\texport $outputfile$")
			return


		else:
			outputFile = pars[0]

			if os.path.isfile(outputFile):
				raise Exception("The output file specified already exists.")

			else:
				try:
					open(outputFile, "w").write(json.dumps(self.variables, indent=2))
					print(f"Variables exported into '{outputFile}'")
				
				except PermissionError:
					raise Exception("Permission denied.")

	def listdir(self, args):
		path = os.getcwd()

		if len(args) > 0:
			path = args[0]

			if not os.path.isdir(path):
				print(graphics.createErrorLog(f"The specified path doesn't exist: {path}"))
				return

		nodes = miscellaneous.getDirNodes(path)

		print(graphics.createTitle("FILES"))
		for file in nodes[0]:
			print("\t" + file)

		print(graphics.createTitle("DIRECTORIES"))
		for directory in nodes[1]:
			print("\t" + directory)








class graphics:
	@staticmethod
	def createErrorLog(msg):
		"""
		Creates a message with the current time and highlights that it is an error
		"""
		return f"[{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second} // ERROR]: {msg}"

	@staticmethod
	def createTitle(msg):
		return f"------------ {msg}"





class syntax:
	@staticmethod
	def separateParsSettings(parameters):
		pars, settings = [], []

		for par in parameters:
			if par.startswith("--"):
				settings.append(par)

			else:
				pars.append(par)

		return {"parameters":pars, "settings": settings}



	@staticmethod
	def parseString(target):
		foo = ""
		target += " "
		result = []
		quoteStatus = False

		if type(target) != str:
			raise Exception("A string was expected.")

		for char in target:

			# Element transition
			if char == " " and not quoteStatus:
				if foo == "":
					continue

				result.append(foo)
				foo = ""
				continue

			# Quotes
			if char == "\"":
				if quoteStatus:
					quoteStatus = False
					continue

				else:
					quoteStatus = True
					continue

			else:
				foo += char
				continue

		return result

	@staticmethod 
	def parseParsedString(string):
		"""
		This function returns a dictionary that contains the already parsed parsed version of the string specified
		\n(command, arguments)
		"""
		command = ""
		arguments = []

		string = syntax.parseString(string)

		if len(string) > 0:
			command = string[0]
			if len(string) > 1:
				arguments = string[1:]


		return {"command":command, "args":arguments}



class miscellaneous:
	@staticmethod
	def getDirNodes(path):
		"""
		Returns the files and folder separated that are in the specified path\n
		The first array are the files and second one are the dirs
		"""

		if not os.path.isdir(path):
			raise Exception("The specified path doesn't exist.")

		else:
			nodes = os.listdir(path)
			result = [[],[]]
			for node in nodes:
				if os.path.isfile(os.path.normpath(path)+ "\\" + node):
					result[0].append(node)
					continue

				else:
					result[1].append(node)

			return result

	@staticmethod
	def checkIfInt(string):
		try:
			int(string)
			return True

		except ValueError:
			return False

if __name__ == "__main__":
	print("This file is a library, cannot be run.")



