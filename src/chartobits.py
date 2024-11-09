import numpy as np

"""
    create a bit stream that takes string as input and outputs bits
    assumes that the message solely consists of ascii characters

    returns an iterator of 0's and 1's 
"""
class BitStream: 
    def __init__(self,string): 
        self.array = []
        for c in string:
            ascii = ord(c) 
            for i in range(6,-1,-1):
                self.array.append((ascii >> i) & 1)
        self.size = len(self.array)
        self.i = 0

    def __iter__(self):
        return self 
    def __next__(self): 
        if self.i == self.size: 
            raise StopIteration

        x = self.array[self.i] 
        self.i = self.i + 1
        return x
    def __str__(self): 
        char = 0 

        letters = []
        for i, bit in enumerate(self.array): 
            print(i)
            char = char ^ (bit << (6-(i%7)))
            if (i + 1) % 7 == 0: 
                letters.append(chr(char))
                char = 0

        return "".join(letters)


def num_to_str(num, zeros): 
    num_binary_string = np.binary_repr(num)
    if zeros: 
        return "".join([chr(0) for i in range(len(num_binary_string))])
    else: 
        num_char = []
        for i in num_binary_string:
            num_char.append(chr(int(i)))

        return "".join(num_char)

def prepend_zeros(limit, num): 
    limit = num_to_str(limit, True)
    num = num_to_str(num, False) 
    return limit[:(len(limit) - len(num))] + num 


if __name__ == '__main__': 
    j = 0;
    num1 = 44010
    num2 = 2 
    print(len(np.binary_repr(num1)))
    print(len(num_to_str(num1, True)))
    print(len(np.binary_repr(num2)))
    print(len(num_to_str(num2, False)))

    message = prepend_zeros(num1, num2) 
    print(len(message))
    print(message)
#    message = "bob"
    for i in BitStream(message): 
        j = j + 1
        if (j % 7 == 0): 
            print(i, np.binary_repr(ord(message[j//7 - 1])), message[j//7 -1])
        else: 
            print(i,end='')
                
    print()
