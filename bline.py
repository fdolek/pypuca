import pandas as pd
import os
import numpy as np
import pickle
import argparse
import time
from optparse import OptionParser
start_time = time.time()


parser = OptionParser()
parser.add_option('-d', '--dataset', help='dataset', dest='dataset')

(options, args) = parser.parse_args()
print(options.dataset)

start_time = time.time()


pkl_file = open(options.dataset + '.pkl', 'rb')
mydata = pickle.load(pkl_file)
pkl_file.close()

bline_dict = {}

for key, value in mydata.items():
    baseline = mydata[key][0:mydata[key].size, 1:100].mean(axis=1)
    print(mydata[key].size)
    Nevent = (baseline.size)
    print('nevent', Nevent)
    blines = baseline.reshape(baseline.size, 1)
    data = (mydata[key] - blines)

    bline_dict.update({key: data})

with open('bline' + options.dataset + '.pkl', 'wb') as fin:
    pickle.dump(bline_dict, fin)

print("--- %.2f seconds ---" % (time.time() - start_time))
