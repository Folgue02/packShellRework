from os import path



def showContent(x, arguments):
	if len(arguments) == 0:
		raise Exception("You didn't specify the target file to display")


	targetFile = arguments[0]

	if not path.isfile(targetFile):
		raise Exception("The file specified cannot be found.")

	else:
		content = open(targetFile, "r").read()
		print(f"Content of file '{targetFile}':\n{content}")



