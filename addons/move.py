import os
import shutil

def moveFile(x, pars):
	
	if "--help" in pars:
		print("Moves an specified file into a location.\nmove $target$ $destiny$ ")
		return

	if len(pars) < 2:
		raise TypeError("move $file$ $destiny$")

	else:
		pars = pars[:2]

		if not os.path.isfile(pars[0]):
			raise FileNotFoundError("The specified file doesn't exist.")

		else:
			
			shutil.move(pars[0], pars[1])
		
			print(f"File '{pars[0]}' moved to '{pars[1]}'")