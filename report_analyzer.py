try:
	import csv
	import sys
	import os
except ImportError as ie:
	print(f"Error during importing {ie.args} module")
	sys.exit(-1)

CSV_DIR = "csv/"

if __name__ == "__main__":
	try:
		NUMBER_OF_ARGUMENTS = 5
		arguments = sys.argv[1:NUMBER_OF_ARGUMENTS]
		trg = arguments[0]
		prd = arguments[1]
		fldnames = arguments[2].split(',') if not len(arguments[2]) == 0 or not arguments[2] == '' else []
		printing_fields = arguments[3].split(',')

		if not len(sys.argv) == NUMBER_OF_ARGUMENTS:
			raise IndexError("ERROR: invalid number of arguments passed at the command line")
	except IndexError as ixe:
		try:
			print(f"{ixe.args}\n\nArguments:\n\ttarget: What set to look in = {trg}\n\tperiod: What period to analyze = {prd}\n\tfieldnames: What fields to get from the set = {fldnames}\n\tprinting_fields: What fields to print = {printing_fields}\n\n", end='')
			if len(sys.argv) > NUMBER_OF_ARGUMENTS:
				inv_args = sys.argv[NUMBER_OF_ARGUMENTS:]
				print("Unrecognized arguments: ", end='')
				for inv_arg in inv_args:
					print(f"{inv_arg};", end=' ')
		except NameError as ne:
			print(ne.args)
		finally:
			sys.exit(-1)
	except Exception as e:
		print(e.args)
		sys.exit(-1)

class ReportAnalyzer:
	__SETS = [
		"PIL",
		"EMP",
		"FAM",
		"NEET",
		"UNEMP",
		"INV",
		"NEETAX",
		"EMPTX",
		"CONS"
	]
	def __init__(self, target, period, fieldnames):
		try:
			if not target in ReportAnalyzer.__SETS:
				raise ValueError("ERROR: the target argument MUST be included among those listed in the doc") 

			if f"{target}_{period}.csv" in os.listdir(path=f"{CSV_DIR}"):
				self.target = target
				self.period = period
				self.path = os.path.join( os.getcwd(), f"{CSV_DIR}{target}_{period}.csv" )
				self.data = self.__read__(self.path, fieldnames)
			else:
				raise FileNotFoundError(f"ERROR: in the {CSV_DIR} dir no corresponding file exists with the actual args")

		except Exception:
			try:
				from traceback import print_exc
				print_exc()
			except ImportError as ie:
				print(f"Error during importing {ie.args} module")
			finally:
				self.data = None

	# Getter methods
	def getData(self):
		return self.data
	def getTarget(self):
		return self.target
	def getPeriod(self):
		return self.period
	def getPath(self):
		return self.path

	# __readSET__ methods
	def __read__(self, path, fieldnames):
		data = {}
		params = []
		n_row = 0
		for fieldname in fieldnames:
			if '=' in fieldname:
				key = fieldname.split('=')[0]
				value = fieldname.split('=')[1]
				params.append(f"{key.strip()}={value.strip()}")
			else:
				params.append(f"{fieldname.strip()}=")

		try:
			with open(path, 'r') as f:
				csvreader = csv.DictReader(f=f)
				for csv_field in csvreader:
					# if params == []:
					# 	data.update({f"{n_row}": csv_field})
					# 	n_row += 1

					for param in params:
						try:
							key = param.split('=')[0]
							value = param.split('=')[1]

							if csv_field[key] == value or value == '':
								data.update({f"{n_row}-{param}": csv_field})
						except KeyError as ke:
							print(f"ERROR: key {ke.args} not found in the csv file")
							continue
						finally:
							n_row += 1
				
				for param in params:
					key = param.split('=')[0]
					value = param.split('=')[1]
					d_fields = []

					for field in data:
						if not data[field][key] == value and not value == '':
							d_fields.append(field)
					
					if bool(d_fields):
						for d_field in d_fields:
							data.pop(d_field)

		except FileNotFoundError as fe:
			print("ERROR: in the path {} no csv file was found with the name provided".format(path))
		except Exception as e:
			print(e.args)

		return data

	def printData(self, args):
		if bool(self.data):
			sep = "\n"
			for key in self.data:
				for arg in args:
					try:
						print(f"{arg}={self.data[key][arg]}, ", end='')
					except KeyError as ke:
						print(f"ERROR: key {ke.args} not found in the dataset, ", end='')
						continue
				print("{}".format(sep), end='')
		else:
			return None

def main():
	ra = ReportAnalyzer(target=trg, period=prd, fieldnames=fldnames)
	data = ra.getData()
	for n in range( len(printing_fields) ):
		printing_fields[n] = printing_fields[n].strip()
	ra.printData(args=printing_fields)

if __name__ == "__main__":
	main()