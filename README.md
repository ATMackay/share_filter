# share_filter

This repository contains Python programs implementating bloom filters for the purposes of tracking partial 
proof of work submissions from mining pool clients. 

For blog containing background information: <insert URL here>

To run you will need to install Python v2.7 or later.

‘share_filter.py’ contains the bloom filter class and block header builder 

‘test_filter.py’ contains scripts that test the bloom filter’s performance for a set of randomly generated submissions

‘bloom_filter_example.py’ is an example using the bloom filter class on a set of randomly generated words 
