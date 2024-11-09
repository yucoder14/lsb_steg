import os, sys, getopt
from enum import Enum
from utils import *

"""
    This program only works with *.png image files
"""
class Mode(Enum): 
    encode = 1
    decode = 2

def check_file_exit(filename): 
    if (os.path.isfile(filename)): 
        return
    else: 
        print(f"file {filename} does not exist")
        sys.exit(2)

def main(): 
    argv = sys.argv[1:]
    
    input_msg = None
    input_png = None
    output_png = None 
    mode = None

    try:
        optlist, args = getopt.getopt(argv, 'e:d:o:i:h')
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    
    for arg, val in optlist: 
        if arg in ['-e']:
            mode = Mode.encode 
            input_png = val 
        elif arg in ['-d']: 
            mode = Mode.decode
            input_png = val 
        elif arg in ['-i']:
            input_msg = val
        elif arg in ['-o']:
            output_png = val 
        elif arg in ['-h']: 
            print("help")

    check_file_exit(input_png)

    if mode == Mode.encode: 
        if (input_msg == None): 
            print("no secret to encode")
            sys.exit(2)
        else: 
            check_file_exit(input_msg)

        if (output_png == None): 
            output_png = f"steg_{input_png}"

        encode_message(input_png, output_png, input_msg)
    elif mode == Mode.decode:        
        length = input("enter message length: ")
        decode_message(input_png, int(length))
    else: 
        print("no modes")

if __name__ == "__main__": 
    main()
