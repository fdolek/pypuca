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

binsize = 2024
data_dict = {}
path_name = '../waveform/'
# path_name = '/eos/project/f/flic2019/Data/XArapuca/run3/'
channels = ['ch0', 'ch1', 'ch10', 'ch11', 'ch2', 'ch3', 'ch8', 'ch9']


i = 0
file_list = []
for filename in sorted(os.listdir(path_name + options.dataset)):
    if '.dat' in filename:
        print(path_name + options.dataset + '/' + filename)
        file_list.append(path_name + options.dataset + '/' + filename)
        fil = pd.concat([pd.read_csv(item, names=[item[1:]]) for item in file_list], axis=1)
        x = pd.DataFrame(fil).to_numpy()
        s = np.transpose(x)
        mod = s.size % binsize
        print ('mod: ',mod)
        Nevent = int(s.size / binsize)
        print('number of event', Nevent)

        arr = s. reshape(Nevent, binsize)
        signal = np.delete(arr, np.s_[0:24], axis=1)

        data_dict.update({channels[i]: signal})
        i += 1
        file_list *= 0

with open(options.dataset + '.pkl', 'wb') as fin:
    pickle.dump(data_dict, fin)

print("--- %.2f seconds ---" % (time.time() - start_time))
