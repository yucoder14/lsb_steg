import os, sys, getopt
from enum import Enum
from utils import *

"""
    This program only works with *.png image files
"""
class Mode(Enum): 
    encode = 1
    decode = 2
    mapout = 3

def check_file_exit(filename): 
    if (os.path.isfile(filename)): 
        return
    else: 
        print(f"file {filename} does not exist")
        sys.exit(2)

def check_if_image(filename): 
    acceptable = ["bmp","dib","jpeg","jpg","jpe","jp2","png","webp","pbm","pgm","ppm","pxm","pnm","sr","ras","tiff","tif","exr","hdr","pic"]
    if (filename.split(".")[-1] in acceptable): 
        return
    else: 
        print(f"file {filename} is not an image")
        sys.exit(2)

def sterilize_string(filename): 
    lossy = ["dib","jpeg","jpg","jpe","jp2","webp","pbm","pgm","ppm","pxm","pnm","sr","ras","tif","exr","hdr","pic"]
    name_array = filename.split(".") 
    if (name_array[-1] in lossy): 
        return name_array[0] + ".png"
    else: 
        return filename

def usage(): 
    print("""Usage: python3 lsb_steg.py [<mode> input_image] [-i input_file] [-o output_image] 

Modes:
    -h      Help mode. This mode does not take any arugments
    -m      Mapout mode. Calculates the 
    -e      Encode mode. Encodes input_file into the input_image
    -d      Decode mode. Decodes the stegged image to retreive secret message

Examples: 
    python3 lsb_steg.py -m input_image.png
    python3 lsb_steg.py -e input_image.png -i input_file.txt
    python3 lsb_steg.py -e input_image.jpg -i input_file.txt -o output_image.png
    python3 lsb_steg.py -d input_image.png 

Notes: 
    Currently, this program can only embed ascii characters into input_image. 
    User must specify the output_image to be a .png file when the input_image is not a .png file
    """)

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
            usage()

    if mode != None:
        check_file_exit(input_img)
        check_if_image(input_img)


    if mode == Mode.encode: 
        if (input_msg == None): 
            print("no secret to encode")
            sys.exit(2)
        else: 
            check_file_exit(input_msg)

        if (output_png == None): 
            output_png = f"steg_{input_img}"

        output_png = sterilize_string(output_png)

        encode_message(input_img, output_png, input_msg)
    elif mode == Mode.decode:        
        decode_message(input_img)
    elif mode == Mode.mapout: 
        get_capacity(input_img)
    else: 
        usage()

if __name__ == "__main__": 
    main()
