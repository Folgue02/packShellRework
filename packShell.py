from sys import argv
import shell
import os
from getpass import getuser
from json import loads, dumps, JSONDecodeError
from colorama import init
from termcolor import colored
from shutil import copyfile
from runscript import scriptExecuter

# This folder is going to contain the most part of the addons that are not builtin
from addons import showContent, curl, move
del argv[0]


class variables:
	DEBUG = False
	packPath = f"C:\\Users\\{getuser()}\\.packShell\\"
	pluginPath = packPath + "addons"
	configFilePath = f"{pluginPath}\\config.json"
	pluginConfig = {}

	pars = shell.syntax.separateParsSettings(argv)["parameters"]
	settings = shell.syntax.separateParsSettings(argv)["settings"]
	requirementsForPlugin = {
		"required":[
			"file",
			"name",
			"pythonFile"
		],
		"optional":[
			"description",
			"help"
		]
	}
	mainShell = shell.shell(
		prompt = f"{colored(getuser(), 'magenta')}@{colored('$D', 'green')}:",
	)


class plugFile:
	@staticmethod
	def readConfigFile():
		return loads(open(variables.configFilePath, "r").read())

	@staticmethod
	def writeConfigFile(content):
		if type(content) != str:
			raise Exception(f"The content specified is not a string, its type is: {type(content)}")

		open(variables.configFilePath, "w").write(content)

	@staticmethod
	def addContent(newContent):
		if not type(newContent) == dict:
			raise Exception("A dictionary was expected.")

		else:
			pluginName = newContent["name"]
			del newContent["name"]


			oldContent = plugFile.readConfigFile()

			# Check if the plugin is already installed.
			if pluginName in oldContent:
				raise Exception("There is already a plugin with that reference name.")

			oldContent[pluginName] = newContent

			# Update the configuration file
			open(variables.configFilePath, "w").write(dumps(oldContent, indent=2))

	@staticmethod
	def deleteContent(commandName):
		"""
		Deletes a plugin specified in the parameters
		"""
		currentContent = plugFile.readConfigFile()
		if not commandName in currentContent:
			raise Exception(f"Plugin '{commandName}' not found in the plugin configuration file.")

		else:
			os.remove(os.path.join(variables.packPath, currentContent[commandName]["file"]))
			del currentContent[commandName]
			plugFile.writeConfigFile(dumps(currentContent, indent=2))



def listPlugins(path, arguments):
	currentConfig = plugFile.readConfigFile()
	
	advancedDisplay = False

	if "--all" in arguments:
		advancedDisplay = True

	x = 0
	print("Available plugins:")
	for plugin in currentConfig:
		print(f"[{x+1}]: {plugin}")
		x += 1
		if advancedDisplay:
			for key in currentConfig[plugin]:
				print(f"\t[{key}]: {currentConfig[plugin][key]}")

			print("\n")


def getPluginHelp(path, arguments):
	currentConfig = plugFile.readConfigFile()

	if len(arguments) == 0:
		raise Exception("You didn't specify the plugin.")

	else:
		plugin = arguments[0]
		if not plugin in currentConfig:
			raise Exception("The plugin specified its not installed, or recognized.")

		else:
			description = "This plugin doesn't have a description"
			helpString = "This plugin doesn't have a guide or some sort of help for the user"

			if "description" in currentConfig[plugin]:
				description = currentConfig[plugin]["description"]

			if "help" in currentConfig[plugin]:
				helpString = currentConfig[plugin]["help"]


			print(f"Plugin description: " + description)
			print(f"Plugin guide: " + helpString)


def removePlugin(path, arguments):

	if len(arguments) == 0:
		raise Exception("You didn't specify the plugin to remove.")

	else:
		plugFile.deleteContent(arguments[0])
		print(f"Plugin totally removed.")



def installPlugin(path, arguments):
	"""
	Installs a plugin based on a configuration file
	"""

	if len(arguments) == 0:
		print(f"You didn't specify the configuration file of the plugin to install.")
		return

	configFile = arguments[0]

	if not os.path.isfile(configFile):
		print(f"Couldn't find the file specified: {configFile}")
		return

	# Read the target file
	try:
		configFile = loads(open(configFile, "r").read())

	except Exception as e:
		print(f"Cannot read the configuration file due to the following error: {e}")
		return


	# Requirements
	for requirement in variables.requirementsForPlugin["required"]:
		if not requirement in configFile:
			print(f"The plugin doesn't have the following requirement: {requirement}")
			return

		else:
			print(f"Requirement satisfied: {requirement}")

	for option in variables.requirementsForPlugin["optional"]:
		if not option in configFile:
			print(f"The plugin doesn't have an optional requirement. ({option})")
		
		else:
			continue

	# Check if the config file already contains the plugin

	if configFile["name"] in configFile:
		print(f"There is already a plugin with the same reference name")
		return

	else:
		pluginName = configFile["name"]
		plugFile.addContent(configFile)
		print("Plugin configuration updated.")
		print("Copying script...")

		copyfile(configFile["file"], os.path.join(variables.packPath, configFile["file"]))


		print(f"Plugin installed as '{pluginName}'.")


def executeSystemCommand(path, pars):
	result = ""


	if len(pars) == 0:
		os.system("cmd")
		return

	for par in pars:
		result += par + " "


	os.system(result)




def executePlugin(path, arguments):
	"""
	This function searches for the specified plugin in the plugin folder
	"""
	command = arguments[0]
	parameters = []

	if len(arguments) == 0:
		return

	if len(arguments) > 1:
		parameters = arguments[1:]
	
	parsedParameters = ""
	currentConfig = plugFile.readConfigFile()
	if command in currentConfig:
		try:
			if variables.DEBUG:
				print("Executing plugin: " + command)

			# Prepares the parameters for being parsed into the shell of the system
			for param in parameters:
				parsedParameters += " " + param

			commandToExecute = variables.packPath + variables.pluginConfig[command]["file"] + parsedParameters

			if currentConfig[command]["pythonFile"]:
				os.system(f"python {commandToExecute}")

			if not currentConfig[command]["pythonFile"]:
				os.system(commandToExecute)

		except Exception as e:
			print(f"Couldn't run the plugin due to the following reason: {e}\nCommand tried to be executed:{variables.pluginConfig[command]['file'] + parsedParameters}")
			return

	else:
		print(f"Cannot recognize the input as a command or order: '{command}'")

	 






def write(path, arguments):
	for arg in arguments:
		print(arg)

def explorePlugins(path, arguments):
	"""
	Opens an explorer window in the path of the plugin configuration file
	"""
	os.system(f"explorer {variables.packPath}")





## Initialization


if "--debug" in variables.settings:
	variables.DEBUG = True

if "--start-directory" in variables.settings:
	if len(variables.pars) == 0:
		print("You must specify the path.")
		exit()

	variables.mainShell.executeInput(f"cd {variables.pars[0]}")



# Needs to be rewrite, it can cause problems due to different folder existance
if not os.path.isdir(variables.packPath) or not os.path.isdir(variables.pluginPath):
	print(f"The packShell path wasn't found, creating it...")
	os.mkdir(variables.packPath)
	os.mkdir(variables.pluginPath)

try:
	variables.pluginConfig = plugFile.readConfigFile()

except JSONDecodeError:
	raise Exception("There is something wrong in the plugin configuration file, maybe its corrupted.")

except FileNotFoundError:
	plugFile.writeConfigFile("{}") # Create an empty configuration file.
	raise Exception("The configuration file didn't exist at the moment the packShell was initialized, now it's been already created.")

if __name__ == "__main__":
	print("Initializing shell...")
	addons = {
		"runplug":executePlugin,
		"explorePlugins":explorePlugins,
		"install":installPlugin,
		"listplugins":listPlugins,
		"removeplugin":removePlugin,
		"help":getPluginHelp,
		"echo":write,
		"run": scriptExecuter(variables.mainShell).ExecuteScript,
		"showcontent": showContent.showContent,
		"cat":showContent.showContent,
		"curl":curl.showWebContent,
		"console":executeSystemCommand,
		"move":move.moveFile
	}
	variables.mainShell.addons = addons
	variables.mainShell.lastCommand = executePlugin




	if variables.DEBUG:
		print("Starting shell in debug mode...")
		variables.mainShell.loopShell()
		exit()


	while True:
		try:
			variables.mainShell.loopShell()

		except KeyboardInterrupt:
			print("You closed the shell.")
			exit()


		except Exception as error:
			print(f"An error has ocurred: {error}")
			continue

