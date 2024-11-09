import numpy as np
import cv2 as cv
from chartobits import *

def bit_splice(ch):  
    bit_planes = []
    for j in range(8): 
        b_plane = np.bitwise_and(2**j,ch)
        shifted = b_plane >> j
        bit_planes.append(shifted)        
    return bit_planes

def merge_bit_planes(row, col, bit_planes): 
    new_ch = np.zeros((row,col), dtype=np.uint8)

    for i, plane in enumerate(bit_planes): 
        new_ch = np.bitwise_or(new_ch, plane << i)

    return new_ch

def show_bit_planes(arr): 
    for i, plane in enumerate(arr):
        cv.imshow(f"{i}",plane*255)

def get_capacity(name):
    img = cv.imread(name)
    row, col, ch = img.shape 

    total_bytes = row * col * ch // 8  
    available_bytes = (total_bytes - len(np.binary_repr(total_bytes)))//1000
    print(f"{name} can contain {available_bytes} KB of text")

def check_sanity(length_bit_string):
    """ 
        Sanity Check to show that length_bit_string correctly encodes the content length

        returns the decoded length of secret message from length_bit_string
    """
    char = 0  
    letters = []
    for i, bit in enumerate(BitStream(length_bit_string)):
        char = char ^ (bit << (6-(i%7)))
        if (i + 1) % 7 == 0: 
            letters.append(int(char))
            char = 0

    length = 0
    for i,bit in (enumerate(reversed(letters))): 
       length = length ^ (bit << i)

    return length

def encode_message(img, new_img, message): 
    img = cv.imread(img)
    row, col, ch = img.shape 

    with open(message, 'r') as file: 
        content = file.read()

    total_bytes = row * col * ch // 8  
    length_bit_string = prepend_zeros(total_bytes, len(content))
    length_str = np.binary_repr(total_bytes)

    assert len(length_bit_string) ==  len(length_str), "these numbers should be equal"

    available_bytes = total_bytes - len(length_str)
    assert len(content) <= available_bytes, "secret file too big!" 

    assert check_sanity(length_bit_string) == len(content), "these numbers should be equal"

    blue, green, red = cv.split(img)

    blue_bit_planes = bit_splice(blue)
    green_bit_planes = bit_splice(green)
    red_bit_planes = bit_splice(red)

    b_coor, g_coor, r_coor = 0, 0, 0

    for i, bit in enumerate(BitStream(length_bit_string + content)):
        match i % 3: 
            case 0: 
                blue_bit_planes[0][b_coor // col][b_coor % col] = bit 
                b_coor = b_coor + 1
            case 1: 
                green_bit_planes[0][g_coor // col][g_coor % col] = bit 
                g_coor = g_coor + 1
            case 2: 
                red_bit_planes[0][r_coor // col][r_coor % col] = bit
                r_coor = r_coor + 1

    new_blue = merge_bit_planes(row, col, blue_bit_planes)
    new_green = merge_bit_planes(row, col, green_bit_planes)
    new_red = merge_bit_planes(row, col, red_bit_planes)

    img = cv.merge((new_blue, new_green, new_red))

    cv.imwrite(new_img, img,[cv.IMWRITE_PNG_COMPRESSION, 9])

    return

def decode_message(img): 
    img = cv.imread(img)
    row, col, ch = img.shape 

    total_bytes = row * col * ch // 8
    length_str = len(np.binary_repr(total_bytes))

    blue, green, red = cv.split(img)

    blue_bit_planes = bit_splice(blue)
    green_bit_planes = bit_splice(green)
    red_bit_planes = bit_splice(red)

    b_coor, g_coor, r_coor = 0, 0, 0

    """ 
        decode length 
    """
    char = 0  
    letters = []
    for i in range(length_str * 7): 
        bit = 0
        match i % 3: 
            case 0: 
                bit = blue_bit_planes[0][b_coor // col][b_coor % col]  
                b_coor = b_coor + 1
            case 1: 
                bit = green_bit_planes[0][g_coor // col][g_coor % col]  
                g_coor = g_coor + 1
            case 2: 
                bit = red_bit_planes[0][r_coor // col][r_coor % col] 
                r_coor = r_coor + 1
        char = char ^ (bit << (6-(i%7)))
        if (i + 1) % 7 == 0: 
            letters.append(int(char))
            char = 0

    assert length_str == len(letters), "These numbers should be equal" 

    length = 0
    for i,bit in (enumerate(reversed(letters))): 
       length = length ^ (bit << i)
    
    char = 0 
    letters = []
    offset = length_str * 7  # we have already iterated this much through the bits
    for i in range(offset, length * 7 + offset): 
        bit = 0
        match i % 3: 
            case 0: 
                bit = blue_bit_planes[0][b_coor // col][b_coor % col]  
                b_coor = b_coor + 1
            case 1: 
                bit = green_bit_planes[0][g_coor // col][g_coor % col]  
                g_coor = g_coor + 1
            case 2: 
                bit = red_bit_planes[0][r_coor // col][r_coor % col] 
                r_coor = r_coor + 1
        char = char ^ (bit << (6-(i%7)))
        if (i + 1) % 7 == 0: 
            letters.append(chr(char))
            char = 0

    print("".join(letters))

    return
