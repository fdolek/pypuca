import re
import os
import gzip
import time
import uproot
import cloudpickle
import numpy as np
from optparse import OptionParser
from multiprocessing import Process

start_time = time.time()

parser = OptionParser()
parser.add_option('-d', '--dataset', help='dataset', dest='dataset')
(options, args) = parser.parse_args()

# arapuca1 = ['channel_132', 'chan

binsize = 2000
data_dict = {}
# path_name = '/home/furkan/data'
file_list = []


def run(runID):

    print('runID:', runID)
    external = uproot.open(runID)['opdigianaExternal']
    # print('test3')
    arapuca1 = ['channel_132', 'channel_133', 'channel_134',
                'channel_135', 'channel_136', 'channel_137',
                'channel_138', 'channel_139', 'channel_140',
                'channel_141', 'channel_142', 'channel_143']

    for xar in arapuca1:
        # print('test4')

        result_array = np.array([])
        for key in external.allkeys():

            # print(runID,key)
            kanal = re.findall("_op(.*?)_waveform", format(key))[0]
            searchResult = re.search(xar, kanal, re.M | re.I)
            if searchResult:
                vector = external[key].values
                # print(vector)
                result_array = np.append(result_array, vector, axis=0)
            eventDump = result_array.reshape(int(result_array.size / binsize),
                                             binsize)
            data_dict.update({xar: eventDump})
    outname = re.findall("np04_raw_(.*?)_waveform", format(runID))[0]
    print(outname)
    # print(data_dict)
    with gzip.open(outname + '_' + '.pkl.gz', 'wb') as fout:
        cloudpickle.dump(data_dict, fout)
    # print('___________________')
    return runID


if __name__ == '__main__':

    for filename in sorted(os.listdir(options.dataset)):
        if '.root' in filename:
<<<<<<< HEAD
            #print('data set plus filename', options.dataset + '/' + filename)
            file_list.append(options.dataset + '/' + filename)
    print('mylist', file_list)
=======
		#print(filename)	
            	print('data set plus filename', options.dataset + '/' + filename)
            	file_list.append(options.dataset + '/' + filename)
    print('my list  :', file_list)
>>>>>>> 58a1627740f0c0b50a74961fd1cd337df2b8da9a

    process = []

    for i in file_list:
        proc = Process(target=run, args=(i,))
        process.append(proc)
        proc.start()
    for p in process:
        p.join()

print("--- %.2f seconds ---" % (time.time() - start_time))
