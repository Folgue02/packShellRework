from shell import syntax


class scriptExecuter:
	def __init__(self, shell):
		self.shell = shell

	def ExecuteScript(self, path, arguments):
		if len(arguments) == 0:
			raise Exception("You didn't specify the script to run.")


		# Read the file
		try:
			targetFile = open(arguments[0], "r")

		except OSError:
			raise Exception("Cannot read the script specified, is it properly spelled?")

		except Exception as e:
			raise Exception("Unknown expception: " + e)

		try:
			for line in targetFile:
				self.shell.executeInput(line.replace("\n",""))

		except KeyboardInterrupt:
			print("The script was terminated.")
			return


