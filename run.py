import os
import time
import pickle
import numpy as np
import pandas as pd
# import numpy.ma as ma
from scipy import stats
from optparse import OptionParser

start_time = time.time()


parser = OptionParser()
parser.add_option('-d', '--dataset', help='dataset', dest='dataset')
(options, args) = parser.parse_args()

binsize = 2024
data_dict = {}
path_name = '/eos/project/f/flic2019/Data/ProtoDUNE_SP/XeDoping_Feb2020/'
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


bline_dict = {}

print('baseline caculation')
for key, value in data_dict.items():
    baseline = data_dict[key][0:data_dict[key].size, 1:100].mean(axis=1)
    # print(data_dict[key].size)
    Nevent = (baseline.size)
    # print(/'nevent', Nevent)
    blines = baseline.reshape(baseline.size, 1)
    data = (data_dict[key] - blines)
    # data1 = data.mean(axis=0)
    # print(data.max(axis=0))
    bline_dict.update({key: data})

del data_dict

select_dict = {}

maskflow = np.ones(10000) == True

# print('test', maskflow.shape)
print('Event selection')
for key, value in bline_dict.items():

    linreg_array = np.array([])
    for row in value[:, 390:420]:
        y = row
        x = np.arange(len(row))

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        trend = r_value * p_value

        mask = [trend > 0]

        linreg_array = np.append(linreg_array, mask, axis=0)
        mask_reg1 = linreg_array > 0
    maskflow = maskflow & mask_reg1

for key, value in bline_dict.items():

    select_dict.update({key: value[maskflow].mean(axis=0)})
    print(key, value[maskflow].shape)
bline_dict
with open(options.dataset + '.pkl.gz', 'wb') as fin:
    pickle.dump(bline_dict, fin)


print("--- %.2f seconds ---" % (time.time() - start_time))
