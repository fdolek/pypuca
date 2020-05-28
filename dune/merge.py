import pandas as pd
import os
import numpy as np
import pickle
import argparse
import time
import cloudpickle
import gzip
from optparse import OptionParser
start_time = time.time()


parser = OptionParser()
parser.add_option('-d', '--dataset', help='dataset', dest='dataset')
(options, args) = parser.parse_args()

my_dict_final = {}  # Create an empty dictionary
path_name = '/eos/project/f/flic2019/Data/ProtoDUNE_SP/XeDoping_Feb2020/allArapuca/'

file_list = []
print('test')

def merge(dirname):

  for filename in sorted(os.listdir(path_name + dirname)):
		if '.pkl.gz' in filename:
			print(filename)
	            	print(path_name + dirname + '/' + filename)
            		file_list.append(path_name + dirname + '/' + filename)
            	for ch in file_list:
			with gzip.open(ch, 'rb') as fout:
				my_dict_final.update(pickle.load(fout))   # Update contents of file1 to the dictionary                
        	print my_dict_final
		with gzip.open(options.dataset + '.pkl.gz', 'wb') as fout:
			cloudpickle.dump(my_dict_final, fout)

merge(options.dataset)
print("--- %.2f seconds ---" % (time.time() - start_time))

