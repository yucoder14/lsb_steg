import numpy as np
import cv2 as cv
from chartobits import BitStream

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

def encode_message(img, new_img, message): 
    img = cv.imread(img)
    row, col, ch = img.shape 

    with open(message, 'r') as file: 
        content = file.read()

    available_bytes = row * col * ch // 8 
    assert len(content) <= available_bytes, "secret file too big!" 

    secret = BitStream(content)

    blue, green, red = cv.split(img)

    blue_bit_planes = bit_splice(blue)
    green_bit_planes = bit_splice(green)
    red_bit_planes = bit_splice(red)

    b_coor = 0
    g_coor = 0
    r_coor = 0

    for i, bit in enumerate(secret):
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

    cv.imwrite(new_img, img)

    return

def decode_message(img, message_length): 
    img = cv.imread(img)
    row, col, ch = img.shape 

    blue, green, red = cv.split(img)

    blue_bit_planes = bit_splice(blue)
    green_bit_planes = bit_splice(green)
    red_bit_planes = bit_splice(red)

    b_coor = 0
    g_coor = 0
    r_coor = 0
    
    char = 0 

    letters = []
    
    for i in range(message_length * 8): 
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
