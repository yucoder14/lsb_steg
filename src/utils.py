import sys

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

