# Python program to build and test Bloom Filter for set words
# Credit: https://www.geeeksforgeeks.org
# Bitarray library rplaced by BitArray (https://pythonhosted.org/bitstring/bitarray.html)
# hash function modified to SAH256

import math
import numpy as np
import hashlib
import random
from bitstring import BitArray



# Bloom Filter Class
class BloomFilter(object): 
  
    ''' 
    Class for Bloom filter, using murmur3 hash function 
    '''
  
    def __init__(self, items_count,fp_prob): 
        ''' 
        items_count : int 
            Number of items expected to be stored in bloom filter 
        fp_prob : float 
            False Positive probability in decimal 
        '''
        # False posible probability in decimal 
        self.fp_prob = fp_prob 
  
        # Size of bit array to use 
        self.size = self.get_size(items_count,fp_prob) 
  
        # number of hash functions to use 
        self.hash_count = self.get_hash_count(self.size,items_count) 
  
        # Bit array of given size 
        self.bit_array = BitArray(self.size)      # MODIFICATION!! BitArray  
  
        # initialize all bits as 0 
        self.bit_array.set(0)      # BitArray
  


    def add(self, item): 
        ''' 
        Add an item in the filter 
        '''
        digests = [] 
        for i in range(self.hash_count): 
  
            # create digest for given item. 
            # i work as seed to SHA256 hash function 
            # With different seed, digest created is different 
            raw_digest = MULTISHA256(item,i)
   
            digest = MULTISHA256(item,i) % self.size   # MODIFIACTION! SHA256 with seed 
            digests.append(digest) 
  
            # set the bit True in bit_array 
            self.bit_array[digest] = True

  
    def check(self, item): 
        ''' 
        Check for existence of an item in filter 
        '''
        for i in range(self.hash_count): 
            digest = MULTISHA256(item,i) % self.size   # MODIFIACTION! SHA256
            if self.bit_array[digest] == False: 
  
                # if any of bit is False then,its not present 
                # in filter 
                # else there is probability that it exist 
                return False
        return True
  
    @classmethod
    def get_size(self,n,p): 
        ''' 
        Return the size of bit array(m) to used using 
        following formula 
        m = -(n * lg(p)) / (lg(2)^2) 
        n : int 
            number of items expected to be stored in filter 
        p : float 
            False Positive probability in decimal 
        '''
        m = -(n * math.log(p))/(math.log(2)**2) 
        return int(m) 
  
    @classmethod
    def get_hash_count(self, m, n): 
        ''' 
        Return the hash function(k) to be used using 
        following formula 
        k = (m/n) * lg(2) 
  
        m : int 
            size of bit array 
        n : int 
            number of items expected to be stored in filter 
        '''
        k = (m/n) * math.log(2) 

        return int(k) 

def SHA256SEED(input, i):                 # SHA256 with salt (integer digest)

    inputseed = str(input)+str(i)         # Concatenate Strings

    return int(hashlib.sha256(inputseed.encode()).hexdigest(), 16)

def MULTISHA256(input, i):                 # SHA256 with salt (integer digest)

    inputseed = str(input)  
    #print('the input is:', input)
    b = hashlib.sha256(inputseed.encode()).hexdigest()
    for k in range(i):
        b = hashlib.sha256(b.encode()).hexdigest()

    return int(b, 16)

# Begin code

n = 20 # Number of items to add
p = 0.05 # False positive probability 

bloomf = BloomFilter(n,p) 
print("Size of bit array:{}".format(bloomf.size)) 
print("False positive Probability:{}".format(bloomf.fp_prob)) 
print("Number of hash functions:{}".format(bloomf.hash_count)) 
  
# words to be added to bloomf
word_present = ['abound','abounds','abundance','abundant','accessable', 
                'bloom','blossom','bolster','bonny','bonus','bonuses', 
                'coherent','cohesive','colorful','comely','comfort', 
                'gems','generosity','generous','generously','genial'] 
  
# word not added 
word_absent = ['bluff','cheater','hate','war','humanity', 
               'racism','hurt','nuke','gloomy','facebook', 
               'geeksforgeeks','twitter'] 
  
for item in word_present: 
    bloomf.add(item) 
  
random.shuffle(word_present) 
random.shuffle(word_absent) 
  
test_words = word_present[:10] + word_absent # Create test input strings

random.shuffle(test_words) 
for word in test_words: 
    if bloomf.check(word): 
        if word in word_absent: 
            print("'{}' is a false positive!".format(word)) 
        else: 
            print("'{}' is probably present!".format(word)) 
    else: 
        print("'{}' is definitely not present!".format(word)) 

 







