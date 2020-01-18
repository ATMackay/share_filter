import time, sys
import math
import numpy as np
import hashlib
import random
from bitstring import BitArray     


def sha256_int(inp):                                        # Return SHA256 hash of input in integer format 
    return int(hashlib.sha256(inp.encode()).hexdigest(), 16)


def multi_sha256(input, i):                                 # Multiple rounds of SHA256 

    if isinstance(input, int):
        inputseed = str(input)
    else:
        raise Exception('input must be integer or string!')    
    b = hashlib.sha256(inputseed.encode()).hexdigest()
    for k in range(i):  
        b = hashlib.sha256(b.encode()).hexdigest()
    b = b[0:10]                                             # Use first 8 bytes of hash digest to reduce CPU cost
    yield int(b,16)


def multi_sha256_old(input, i):                                 # Multiple rounds of SHA256 

    if isinstance(input, int):
        inputseed = str(input)
    else:
        raise Exception('input must be integer or string!')    
    b = hashlib.sha256(inputseed.encode()).hexdigest()
    for k in range(i):
        b = hashlib.sha256(b.encode()).hexdigest()
    b = b[0:10]                                             # Use first 8 bytes of hash digest to reduce CPU cost
    return int(b, 16)


a = np.random.randint(1,1000000000)
b = 1000

start = time.time()
a1 = multi_sha256(a, b)
print(next(a1))
finish = time.time()
print("\nTime taken new:{}".format(finish - start))

start = time.time()
a2 = multi_sha256_old(a, b)
print(a2)
finish = time.time()
print("\nTime taken old:{}".format(finish - start))

quit()
