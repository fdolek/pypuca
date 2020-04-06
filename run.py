import pandas as pd
import os
import numpy as np
import pickle
import time
from optparse import OptionParser
import numpy.ma as ma

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

for key, value in data_dict.items():
    baseline = data_dict[key][0:data_dict[key].size, 1:100].mean(axis=1)
    print(data_dict[key].size)
    Nevent = (baseline.size)
    print('nevent', Nevent)
    blines = baseline.reshape(baseline.size, 1)
    data = (data_dict[key] - blines)

    satur = ma.masked_greater(data, 14000)
    sdata = np.ma.compress_rowcols(satur, 0)

    linreg_array = np.array([])
    for row in sdata[:, 390:420]:
        y = row
        x = np.arange(len(row))

        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        trend= r_value * p_value

        mask = [trend > 0 ]

        linreg_array = np.append(linreg_array, mask, axis=0)
        mask_reg1=linreg_array > 0

    linreg_array = np.array([])
    for row in sdata[:,390:420]:
        y = row
        x = np.arange(len(row))

        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        trend = r_value * p_value
        mask = [r_value > 0.6 ]

        linreg_array  = np.append(linreg_array , mask, axis=0)
        mask_reg2 = linreg_array  > 0
    evtselect=sdata[mask_reg1*mask_reg2]
    print(evtselect.shape)

    # print(int(sdata.size/2000))
    data = evtselect.mean(axis=0)
    # data1 = data.mean(axis=0)
    # print(data.max(axis=0))
    bline_dict.update({key: data})

with open(options.dataset + '.pkl', 'wb') as fin:
    pickle.dump(bline_dict, fin)


print("--- %.2f seconds ---" % (time.time() - start_time))
