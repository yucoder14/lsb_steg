import os, sys, getopt
from enum import Enum
import steg
import utils

class Mode(Enum): 
    encode = 1
    decode = 2
    mapout = 3

def main(): 
    argv = sys.argv[1:]
    
    input_msg = None
    input_img = None
    output_png = None 
    mode = None

    try:
        optlist, args = getopt.getopt(argv, 'e:d:o:i:hm:')
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    
    for arg, val in optlist: 
        if arg in ['-e']:
            mode = Mode.encode 
            input_img = val 
        elif arg in ['-d']: 
            mode = Mode.decode
            input_img = val 
        elif arg in ['-m']:
            mode = Mode.mapout
            input_img = val
        elif arg in ['-i']:
            input_msg = val
        elif arg in ['-o']:
            output_png = val 
        elif arg in ['-h']: 
            utils.usage()

    if mode != None:
        utils.check_file_exit(input_img)
        utils.check_if_image(input_img)


    if mode == Mode.encode: 
        if (input_msg == None): 
            print("no secret to encode")
            sys.exit(2)
        else: 
            utils.check_file_exit(input_msg)

        if (output_png == None): 
            output_png = f"steg_{input_img}"

        output_png = utils.sterilize_string(output_png)

        steg.encode_message(input_img, output_png, input_msg)
    elif mode == Mode.decode:        
        steg.decode_message(input_img)
    elif mode == Mode.mapout: 
        steg.get_capacity(input_img)
    else: 
        utils.usage()

if __name__ == "__main__": 
    main()
