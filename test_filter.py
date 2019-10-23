# Python program for testing share_filter against random input data
from share_filter import *
import numpy as np
import hashlib
import random
import sys
import time


# Progress Bar
def update_progress(job_title, progress):
    length = 100                                                      # modify this to change the length
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100, 4))
    if progress >= 1: msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()

# 
def test_tracker_size(trials, nonce_range, false_pos_prob):           # Tests bloom filter for random nonce values from 1 to N 
    start = time.time()
    bloomf = BloomFilter(trials, false_pos_prob)


    hash_list = list()                                                # Create list to store submissions. This will be used to compare 
    duplicates = list()                                               # Create list to store repeated submission (including false positives)
    false_positive = list()                                           # create list to store false positives

                                                                      # Test new element against bloom filter and keep track of performance using hash list
    for i in range(trials):
        update_progress("Testing share_tracker memory footprint: ", float(i)/trials)
        nonce = random.randint(1, nonce_range)                        # Create dummy nonce inputs 
        item = sha256_int(create_block_header(nonce))               # Item is the hash of the nonce (would be hash of block header in real thing)

        if bloomf.check(item):                                        # Check hash against Bloom Filter
           duplicates.append(item)                                    # Add to list of duplicate submissions                      
           if nonce in hash_list:                                     # List check
                continue  
           else: 
                false_positive.append(item)                           # Item is a false positive 
        else:
            bloomf.add(item)                                          # Add item to bloom filter

        hash_list.append(item)                                        # Add submission to list


    badhashperc = float(len(duplicates))/float(trials)*100
    falseposperc = float(len(false_positive))/float(trials)*100
    actual_badhashperc =  badhashperc - falseposperc

    list_size = sys.getsizeof(hash_list)                              # Size of hash list
    bloom_size = sys.getsizeof(bloomf)                                # Size of Bloom filter
    ratio = bloom_size/list_size

    # Print results in command window 
    print("\n \nExpected submissions:{}".format(trials))  
    print("B.F. False positive Probability:{}".format(bloomf.fp_prob)) 
    print("B.F. Number of hash functions:{}".format(bloomf.hash_count)) 

    print("\nBloom Filter size (bytes):{}".format(bloom_size))
    print("List size (bytes):{}".format(list_size))
    print("Comresssion Ratio:{}".format(1.0/ratio)) 
    print("Memory reduction %:{}".format((1.0-ratio)*100))

    print("\nRepeated submission percentage (Bloom filter):{}".format(badhashperc))    
    print("\nRepeated submission percentage (Hash list):{}".format(actual_badhashperc))   
    finish = time.time()
    if len(duplicates)==0:
        return "no false positives in "+str(trials)+" random hashes"
    else: 
        return ('Test of %s trial submissions finished in %s seconds' % (trials, finish - start)) 



def test_tracker_speed(trials, nonce_range, false_pos_prob):          # Tests bloom filter for random nonce values from 1 to nonce_range 
    start = time.time()
    bloomf = BloomFilter(trials, false_pos_prob)                      # construct Bloom filter

    hash_list = list()                                                # List to storing all new submissions. 
    bloom_bad_hash = list()                                           # List storing hashes rejected by the bloom filter (including false positives)
    list_bad_hash = list()                                            # List storing repeated submissions 
    false_positive = list()                                           # List storing false positives


    bloom_start = time.time()                                                                     
    for i in range(trials):
        update_progress("Testing share_tracker speed: ", 0.5*float(i)/trials)
        nonce = random.randint(1, nonce_range)                        # Create dummy nonce inputs 
        item = sha256_int(create_block_header(nonce))                 # Item is the hash of the block header including nonce 

        if bloomf.check(item):                                        # Check hash against Bloom Filter
           continue                                                   # Discard duplicate submissions                      
        else:
           bloomf.add(item)                                           # Add item to bloom filter
    bloom_finish = time.time()


    # Begin hash list check
    list_start = time.time()
    for i in range(trials):
        update_progress("Testing share_tracker speed: ", 0.5*float(i)/trials+0.5)
        nonce = random.randint(1, nonce_range)                        # Create dummy nonce inputs 
        item = sha256_int(create_block_header(nonce))               # Item is the hash of the block header including nonce 

        if item in hash_list:                                         # Check hash against hash list
           continue                                                   # Discard  duplicate submissions                      
        else:
           hash_list.append(item)                                     # Add item to bloom filter
    list_finish = time.time()

    ratio = (bloom_finish - bloom_start)/(list_finish - list_start)

    # Print results in command window 
    print("\n \nExpected submissions:{}".format(trials))  
    print("B.F. False positive Probability:{}".format(bloomf.fp_prob)) 
    print("B.F. Number of hash functions:{}".format(bloomf.hash_count)) 


    print("\nTime taken to check bloom filter:{}".format(bloom_finish - bloom_start))    
    print("\nTime taken to check hash list:{}".format(list_finish - list_start))
    print("\n Percentage reduction:{}".format((1.0-ratio)*100))    
    finish = time.time()
    return ('Test of %s trial submissions finished in %s seconds' % (trials, finish - start)) 



# Test input data
n_range = 1000000000
trls = [50000, 100000, 500000, 1000000]
f_prob = [0.01, 0.001, 0.0005]

# Generate test size results

def main(size, speed):

    if size == True:
        # Generate test memory data
        for i in range(len(trls)):
            for j in range(len(f_prob)):
                print(test_tracker_size(trls[i], n_range, f_prob[j]))
    if speed == True:
        # Generate test speed data
        for i in range(len(trls)):
            for j in range(len(f_prob)):
                print(test_tracker_speed(trls[i], n_range, f_prob[j]))



if __name__== "__main__":
    main(False, True)

    end()









