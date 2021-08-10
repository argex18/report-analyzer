try:
    import matplotlib as mpl
    import numpy as np
except ImportError as ie:
    print("Error while importing matplotlib or numpy:\nDid you forget to install them? Did you forget to activate a virtual environment?")
    from sys import exit
    exit(-1)

import sys
import os.path

if __name__ == "__main__":
    try:
        MAX_NUMBER_OF_ARGUMENTS = 2
        arguments = sys.argv[1:]
        gphs = arguments[0].split(',')
        lbls = arguments[1].split(',')

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
            "labels": None
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
    def __init__(self, graphs, labels):
        try:
            if not isinstance(graphs, list) or not isinstance(labels, list):
                raise TypeError("Error while parsing constructor arguments: graphs and labels MUST be instance of list")

            self.graphs = tuple(self.__remove_whitespaces(graphs))
            self.labels = tuple(self.__remove_whitespaces(labels))
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
                        raise ValueError(f"{args[n]} is not instance of str")

                    args[n] = args[n].strip()
                except Exception as e:
                    for arg in e.args:
                        print(arg)
                    continue
            return args
        except Exception as e:
            for arg in e.args:
                print(arg)
            return None
    
    def getCsvData(self):
        try:
            from report_analyzer import ReportAnalyzer
        except ImportError as ie:
            print("Error while importing report_analyzer module")
            sys.exit(-1)

        csv_data = None
        try:
            ra = ReportAnalyzer("PIL", "2019-2021", ["Valutazione=variazione congiunturale"])
            ra.printData(["Value", "TIME"])
            csv_data = ra.getData()
        except Exception:
            pass
        finally:
            return csv_data


def main():
    gc = GraphComposer(graphs=gphs, labels=lbls)
    # print(gc.graphs)
    # print(gc.labels)

    csv_data = gc.getCsvData()
    # print(csv_data)

if __name__ == "__main__":
    main()