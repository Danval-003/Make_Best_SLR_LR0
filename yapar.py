import argparse

from YaPar_reader.yapar_reader import yaPar_reader
from tools import *
import pickle

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compile a program')
    parser.add_argument('source', help='Source file')
    parser.add_argument('-o', help='Output file', default=None)
    parser.add_argument('-s', help='Script file', default=None)
    args = parser.parse_args()
    content = reader(args.source)
    reader2 = yaPar_reader(content)
    reader2.organize()
    reader2.LROrganize()
    reader2.graphLRO()
    tableSlr = reader2.getSLRTable()
    file_name = args.o if args.o else args.source.split('.')[0] + '.pickle'
    file_script = args.s if args.s else args.source.split('.')[0]+'.py'

    # Exportar el objeto a un archivo pickle
    with open(file_name, 'wb') as file_pickle:
        pickle.dump(tableSlr, file_pickle)

    print(f'File {file_name} created')

    with open(file_name, 'rb') as file_pickle:
        tableSlr2 = pickle.load(file_pickle)

    code = f"""
import argparse
import pickle
import subprocess
from YaPar_reader.SLR_simulater import SLR_simulate
from YaPar_reader.yapar_reader import yaPar_reader
from tools.Reader import reader    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compile a program')
    parser.add_argument('-oScan', help='Output scan file', default=None)
    args = parser.parse_args()
    with open("{file_name}", 'rb') as yaparFile:
        tableSLR = pickle.load(yaparFile)
        
    content = reader(args.oScan)
    SLR_simulate(content, tableSLR)
    
    """

    with open(file_script, 'w') as fileScript:
        fileScript.write(code)





