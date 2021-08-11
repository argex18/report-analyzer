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
		"['-f', '--fieldnames'] => set the fieldnames to extract from the dataset\n\t" \
		"['-s', '--printingfields'] => set the fields to print\n\n"

if __name__ == "__main__":
	try:
		arguments = {
			"options": {
				"h": "help",
				"v": "verbose"
			},
			"target": {
				"short_opt": "t:",
				"long_opt": "target=",
				"value": None
			},
			"period": {
				"short_opt": "p:",
				"long_opt": "period=",
				"value": None
			},
			"fieldnames": {
				"short_opt": "f:",
				"long_opt": "fieldnames=",
				"value": None
			},
			"printingfields": {
				"short_opt": "s:",
				"long_opt": "printingfields=",
				"value": None
			}
		}
		options = {
			"short": [],
			"long": []
		}
		for n_key in arguments.keys():
			if n_key == "options":
				options["short"] = options["short"] + list(arguments[n_key].keys())
				options["long"] = options["long"] + list(arguments[n_key].values())
			else:
				options["short"].append(arguments[n_key]["short_opt"])
				options["long"].append(arguments[n_key]["long_opt"])

		opts, args = getopt.getopt(
			sys.argv[1:],
			''.join(options["short"]),
			options["long"]
		)

		for option, arg in opts:
			if option in ("-h", "--help"):
				print(USAGE, end='')
				sys.exit(0)
			elif option in ("-v", "--verbose"):
				verbose = True
			elif option in ("-t", "--target"):
				arguments["target"]["value"] = arg
			elif option in ("-p", "--period"):
				arguments["period"]["value"] = arg
			elif option in ("-f", "--fieldnames"):
				arguments["fieldnames"]["value"] = arg.split(',')
			elif option in ("-s", "--printingfields"):
				arguments["printingfields"]["value"] = arg.split(',')
			else:
				assert False, "not recognized option"

		if arguments["target"]["value"] is None or arguments["period"]["value"] is None:
			raise ValueError("ERROR: mandatory arguments not specified")

	except getopt.GetoptError as ge:
		print(f"ERROR: option {ge.opt} results in '{ge.msg}'")
		print(USAGE, end='')
		sys.exit(-1)
	except ValueError as ve:
		print(USAGE, end='')
		for exc in ve.args:
			print(exc)
		print(f"Mandatory arguments:\n\t"
			  f"target = {arguments['target'].items()},\n\t"
			  f"period = {arguments['period'].items()},\n\n", end='')
		print(f"Optional arguments:\n\t"
			  f"fieldnames = {arguments['fieldnames'].items()}\n\t"
			  f"printingfields = {arguments['printingfields'].items()}\n\n", end='')
		sys.exit(-1)
	except Exception as e:
		for exc in e.args:
			print(exc)
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
			if target not in ReportAnalyzer.__SETS:
				raise ValueError(
					"ERROR: the target argument MUST be included among those listed in the doc",
					target)

			if f"{target}_{period}.csv" in os.listdir(path=f"{CSV_DIR}"):
				self.target = target
				self.period = period
				self.path = os.path.join(os.getcwd(), f"{CSV_DIR}{target}_{period}.csv")
				self.data = self.__read(self.path, fieldnames)
			else:
				raise FileNotFoundError(
					f"ERROR: in the {CSV_DIR} dir no corresponding file exists with the actual args",
					target, period)

		except ValueError as verrs:
			for verr in verrs.args:
				print(verr)
			self.data = None
		except FileNotFoundError as ferrs:
			for ferr in ferrs.args:
				print(ferr)
			self.data = None
		except Exception:
			from traceback import print_exc
			print_exc()
			self.data = None

	# Getter methods
	def get_data(self):
		return self.data

	def get_target(self):
		return self.target

	def get_period(self):
		return self.period

	def get_path(self):
		return self.path

	# __readSET__ methods
	@staticmethod
	def __read(path, fieldnames):
		data = {}
		params = []
		n_row = 0

		if fieldnames is None:
			fieldnames = []

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

					if params:
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
					else:
						data.update({f"{n_row}": csv_field})
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

			return data

		except FileNotFoundError:
			print("ERROR: in the path {} no csv file was found with the name provided".format(path))
			return {}
		except Exception as errs:
			for err in errs.args:
				print(err)
			return {}

	def print_data(self, p_fields):
		if bool(self.data):
			sep = "\n"
			for key in self.data:
				if not p_fields:
					print(f"{self.data[key]}, ", end='')

				for p_field in p_fields:
					try:
						print(f"{p_field}={self.data[key][p_field]}, ", end='')
					except KeyError as ke:
						print(f"ERROR: key {ke.args} not found in the dataset, ", end='')
						continue
				print("{}".format(sep), end='')
		else:
			return None


def main():
	trg, prd, fldnames, printing_fields = arguments["target"]["value"],\
										  arguments["period"]["value"],\
										  arguments["fieldnames"]["value"],\
										  arguments["printingfields"]["value"]
	ra = ReportAnalyzer(target=trg, period=prd, fieldnames=fldnames)
	if printing_fields is not None and isinstance(printing_fields, list):
		for n in range(len(printing_fields)):
			printing_fields[n] = printing_fields[n].strip()
	else:
		printing_fields = []
	ra.print_data(p_fields=printing_fields)


if __name__ == "__main__":
	main()
