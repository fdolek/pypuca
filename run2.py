import os
import time
import pickle
import numpy as np
import pandas as pd
# import numpy.ma as ma
from optparse import OptionParser

start_time = time.time()


parser = OptionParser()
parser.add_option('-d', '--dataset', help='dataset', dest='dataset')
(options, args) = parser.parse_args()

binsize = 2024
data_dict = {}
path_name = '/eos/project/f/flic2019/Data/ProtoDUNE_SP/XeDoping_Feb2020/data/'
# path_name = '/eos/project/f/flic2019/Data/XArapuca/run3/'
# channels = ['ch0', 'ch1', 'ch10', 'ch11', 'ch2', 'ch3', 'ch8', 'ch9']
channels = ['Ch1', 'Ch2', 'Ch3', 'Ch4', 'Ch5', 'Ch7']

i = 0
file_list = []
for filename in sorted(os.listdir(path_name + options.dataset)):
    if '.dat' in filename:
        print(path_name + options.dataset + '/' + filename)
        file_list.append(path_name + options.dataset + '/' + filename)
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

with open(options.dataset + '.pkl.gz', 'wb') as fin:
    pickle.dump(data_dict, fin)
    # pickle.dump(select_dict, fin)
    # pickle.dump(data_dict, fin)

print("--- %.2f seconds ---" % (time.time() - start_time))
