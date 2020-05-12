from urllib import request, error
from os import path

def showWebContent(cwd, args):
	if len(args) == 0:
		raise Exception("The web page wasn't specified")

	if "--help" in args:
		print("Command usage: curl [page] [option] [optional parameter]")
		print("""
Available options:
	--help 
		Displays this message

	--save
		Saves the content of the target in a file (In this case you must specify the name of the file you want to use to save the information in the position of 'optional parameter')
			""")
		return

	# Read the web page
	try:
		page = request.urlopen(args[0])
	except error.URLError:
		raise Exception("Cannot read the webpage you have specified.")
	
	# Option to save the content in a file
	if "--save" in args:

		# In this case there must be a name of the file where you are going to save the content
		if len(args) < 3:
			raise Exception("You must specify the name of the file where you are going to save the content.")

		else:
			if path.isfile(args[2]):
				raise Exception("There is already a file named like that.")

			else:
				
				open(args[2], "w").write(str(page.read()))
				print(f"Content saved in file '{args[2]}'")
				return

	else:
		print(f"Content of '{args[0]}'")
		print(page.read())
		print("END")