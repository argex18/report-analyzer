try:
    import matplotlib as mpl
    import numpy as np
except ImportError as ie:
    print("Error while importing matplotlib or numpy:\n"
          "Did you forget to install them? Did you forget to activate a virtual environment?")
    from sys import exit
    exit(-1)

import sys
import os.path
try:
    from report_analyzer import ReportAnalyzer
except ImportError:
    print("Error while importing report_analyzer module")
    sys.exit(-1)

if __name__ == "__main__":
    try:
        MAX_NUMBER_OF_ARGUMENTS = 5
        arguments = sys.argv[1:]
        gphs = arguments[0].split(',')
        lbls = arguments[1].split(',')
        trgs = arguments[2].split(',')
        prds = arguments[3].split(',')
        flds = arguments[4].split(';')

        if len(arguments) > MAX_NUMBER_OF_ARGUMENTS:
            raise NameError()
    except NameError as ne:
        un_args = arguments[MAX_NUMBER_OF_ARGUMENTS:]
        print("Unrecognized arguments: ", end='')
        for un_arg in un_args:
            print(f"{un_arg}, ", end='')
        sys.exit(-1)
    except IndexError as ie:
        n = 0
        parameters = {
            "graphs": None,
            "labels": None,
            "targets": None,
            "periods": None,
            "fields": None
        }
        print("Not found arguments: ", end='')
        for parameter in parameters:
            try:
                parameters[parameter] = arguments[n]
            except IndexError:
                print(f"{parameter}[{n}], ", end='')
            finally:
                n += 1
        sys.exit(-1)
    except Exception as e:
        for arg in e.args:
            print(arg)
        sys.exit(-1)

class GraphComposer:
    def __init__(self, graphs, labels, targets, periods, fields):
        try:
            if not isinstance(graphs, list) or not isinstance(labels, list) or not isinstance(targets, list)\
                    or not isinstance(periods, list) or not isinstance(fields, list):
                raise TypeError("Error while parsing constructor arguments: all arguments MUST be instance of list")

            self.graphs = tuple(self.__remove_whitespaces(graphs))
            self.labels = tuple(self.__remove_whitespaces(labels))
            self.targets = tuple(self.__remove_whitespaces(targets))
            self.periods = tuple(self.__remove_whitespaces(periods))
            self.fields = tuple(self.__remove_whitespaces(fields))
        except Exception as e:
            for arg in e.args:
                print(arg)
            self.graphs = None
            self.labels = None
    
    def __remove_whitespaces(self, args):
        try:
            for n in range(0, len(args)):
                try:
                    if not isinstance(args[n], str):
                        raise ValueError(f"Error while parsing {args[n]}")

                    args[n] = args[n].strip()
                except ValueError as ve:
                    for arg in ve.args:
                        print(arg)
            return args
        except Exception as e:
            for arg in e.args:
                print(arg)
            return None
    
    def getCsvData(self):
        try:
            csv_data = []

            for target, period, fieldnames in zip(self.targets, self.periods, self.fields):
                ra = ReportAnalyzer(target=target, period=period, fieldnames=fieldnames.split(','))
                csv_data.append(ra.getData())

            return csv_data

        except Exception as e:
            for arg in e.args:
                print(arg)

            return []


def main():
    gc = GraphComposer(graphs=gphs, labels=lbls, targets=trgs, periods=prds, fields=flds)
    # print(gc.graphs)
    # print(gc.labels)

    csv_data = gc.getCsvData()
    print(csv_data)

if __name__ == "__main__":
    main()