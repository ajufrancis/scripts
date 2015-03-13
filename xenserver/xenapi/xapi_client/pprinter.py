import pprint

def pprinter(data):
    pp = pprint.PrettyPrinter()
    output = pp.pprint(data)
    return output
