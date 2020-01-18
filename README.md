# share_filter

share_filter is a Python program implementating bloom filter enabled tracking of partial 
proof of work submissions. Note, this is a proof of concept used to obtain empirical data supporting research on the use of bloom filters for effieicnt set membership tests.

For blog containing background information: https://medium.com/@alexandertennysonmackay/filtering-shares-scaling-mining-pool-software-with-boom-filters-949b1ae91ea1.

To run you will need to install Python v2.7 or later.

‘share_filter.py’ contains the bloom filter class and block header builder. 

‘test_filter.py’ contains scripts that test the bloom filter’s performance for a set of randomly generated submissions.

‘bloom_filter_example.py’ is an example using the bloom filter class on a set of randomly generated words.

Copyright 2019 Alexander Mackay

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
