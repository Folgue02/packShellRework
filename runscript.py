from shell import syntax
import os

class scriptExecuter:
	def __init__(self, shell):
		self.shell = shell

	def ExecuteScript(self, path, arguments):
		# Executes a group of orders stored in an specified file.
		if len(arguments) == 0:
			raise Exception("You didn't specify the script to run.")


		# Read the file
		try:
			targetFile = open(arguments[0], "r")

		except OSError:
			raise Exception("Cannot read the script specified.")

		except Exception as e:
			raise Exception("Unknown expception: " + e)

		try:
			for line in targetFile:
				self.shell.executeInput(line)

		except KeyboardInterrupt:
			print("The script was terminated.")
			return



	def importFunction(self, x, arguments):
		# Creates a command // func by gathering the orders from a file.

		if "--help" in arguments:
			print("Creates a command by storing the orders from a script.")
			print("\timportfunc $file$ $commandname$")
			return

		if len(arguments) < 2:
			raise Exception("Not enough arguments specified.")

		else:
			path = arguments[0]
			commandName = arguments[1]

			if len(arguments) > 1:
				args = arguments[1:]

			if not os.path.isfile(path):
				raise FileNotFoundError(f"File '{path}' couldn't be found.")

			file = open(arguments[0], "r")

			parsedOrders = [line.replace("\n", "") for line in file]
			self.shell.customCommands[commandName] = parsedOrders

	def runFunction(self, command, arguments):
		# Executes a func stored

		targetFunction = self.shell.customCommands[command]

		for order in targetFunction:
			self.shell.executeInput(order)

