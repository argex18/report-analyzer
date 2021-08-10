try:
	import csv, sys, os, argparse, getopt
except ImportError as ie:
	print(f"Error during importing {ie.args} module")
	sys.exit(-1)

CSV_DIR = "csv/"
USAGE = "BASIC USAGE of report-analyzer:\n\t" \
		"['-h', '--help'] => show info about the script\n\t" \
		"['-t', '--target'] => set the target dataset on which to execute the analysis\n\t" \
		"['-p', '--period'] => set the period on which to perform the analysis\n\t" \
		"['-f', '--fieldnames'] => set the fieldnames to extract from the set\n\t" \
		"['--printingfields'] => set the fields to print\n"

if __name__ == "__main__":
	try:
		arguments = sys.argv[1:]
		options, args = getopt.getopt(
			arguments,
			"hvt:p:f:s:",
			["help", "verbose", "target=", "period=", "fieldnames=", "printingfields="]
		)
		for option, arg in options:
			if option in ("-h", "--help"):
				print(USAGE, end='')
				sys.exit(0)
			elif option in ("-v", "--verbose"):
				verbose = True
			elif option in ("-t", "--target"):
				trg = arg
			elif option in ("-p", "--period"):
				prd = arg
			elif option in ("-f", "--fieldnames"):
				fldnames = arg.split(',')
			elif option in ("-s", "--printingfields"):
				printing_fields = arg.split(',')
			else:
				assert False, "not recognized option"

		# print(len(args))

	except getopt.GetoptError as ge:
		print(f"ERROR: option {ge.opt} results in '{ge.msg}'")
		print(USAGE, end='')
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
	# def getTarget(self):
	# 	return self.target
	# def getPeriod(self):
	# 	return self.period
	# def getPath(self):
	# 	return self.path

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
