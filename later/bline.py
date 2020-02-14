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
#channels = ['ch1', 'ch10', 'ch11', 'ch2', 'ch3', 'ch8', 'ch9']
#channels=['Ch1','Ch10','Ch11','Ch1','Ch2','Ch3','Ch4','Ch5','Ch6','Ch7','Ch8']

def pkl(dirname):
    i = 0
    file_list = []
    for filename in sorted(os.listdir(path_name + dirname)):
        if '.dat' in filename:
            print(path_name + dirname + '/' + filename)
            file_list.append(path_name + dirname + '/' + filename)
            fil = pd.concat([pd.read_csv(item, names=[item[1:]]) for item in file_list], axis=1)
            x = pd.DataFrame(fil).to_numpy()
            s = np.transpose(x)
            Nevent = int(s.size / binsize)
            print('number of event', Nevent)

            arr = s. reshape(Nevent, binsize)
            signal = np.delete(arr, np.s_[0:24], axis=1)

            data_dict.update({channels[i]: signal})
            i += 1
            file_list *= 0



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
