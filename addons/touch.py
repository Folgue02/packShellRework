import os

def touchFile(x, pars):
	if len(pars) == 0:
		print("No file specified.")
	
	if pars[0] == "--help":
		print("This command creates a blank file. Usage:" )
		print("\ttouch $file$")
		return
	
	else:
		if os.path.isfile(pars[0]):
			raise Exception("The file already exists.")
		
		else:
			try:
				open(pars[0]).write("")
			except PermissionError:
				raise Exception("Cannot create the file, permission denied.")
