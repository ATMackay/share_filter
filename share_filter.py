# Python program to build Bloom filter for tracking partial proof of work shares
# Bloom filter class credit: https://www.geeeksforgeeks.org
# Bitarray library replaced by BitArray (https://pythonhosted.org/bitstring/bitarray.html)
# run  $ easy_install bitstring
# Or alternatively
# run  $ pip install bitstring
import math
import numpy as np
import hashlib
import random
from bitstring import BitArray     



def SHA256(input):
    bin_input = "{0:b}".format(input)  #Converts to binary before hashing

    return hashlib.sha256(binput.encode()).hexdigest()

def sha256_int(inp):

    #bin_input = "{0:b}".format(inp)  #Converts to binary before hashing

    return int(hashlib.sha256(inp.encode()).hexdigest(), 16)



def multi_sha256(input, i):                 # SHA256 with salt (integer digest)

    if isinstance(input, int):
        inputseed = str(input)
    else:
        raise Exception('input must be integer or string!')    

    b = hashlib.sha256(inputseed.encode()).hexdigest()
    for k in range(i):
        b = hashlib.sha256(b.encode()).hexdigest()

    return int(b, 16)

# Bloom Filter Class (Modified hash functions)
class BloomFilter(object): 
  
    ''' 
    Class for Bloom filter, using SHA256 hash function 
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

            digest = multi_sha256(item,i) % self.size  
            digests.append(digest) 
  
            # set the bit True in bit_array 
            self.bit_array[digest] = True

    def check(self, item): 
        ''' 
        Check for existence of an item in filter 
        '''
        for i in range(self.hash_count): 
            digest = multi_sha256(item,i) % self.size   
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



def share_tracker(blockheader_submission):
    if BloomFilter.check(blockheader_submission)==False:
       BloomFilter.add(blockheader_submission)
       return True
    else:
        return False    

    


# Create block template from single nonce input 
# Note: In practice the block constructor will use the extra nonce to recalculate the Merkle root, this is just a 

def create_block_template(nonce):                                                           # Creates block header bytestring ready to be hashed (Elements hard coded from block 582995)
    version = '0x20000000'                                                                  # Version number (HARD CODED)
    prev_block_hash = '0x000000000000000008811f50b64684257e8821114783e245af1e7f6a0909ef99'  # Hash of previous block header (HARD CODED)
    merkle_root = '0xebd2fb876da201b8788f1df43518f75e48d0a99cad415a9b55d7ab31a56e24ee'      # Merkle root (HARD CODED)
    timestamp = hex(1558243426)                                                             # Timestamp (HARD CODED) 
    nBits = '0x18105e9f'                                                                    # Target    (HARD CODED)
    nNonce = hex(nonce)

    bin_version = version[2:]
    bin_prev_block_hash = prev_block_hash[2:]
    bin_merkle_root = merkle_root[2:]
    bin_timestamp = timestamp[2:]
    bin_nBits = nBits[2:]
    bin_nNonce = nNonce[2:]	

    block_header = bin_version + bin_prev_block_hash + bin_merkle_root + bin_timestamp + bin_nBits + bin_nNonce

    return block_header




