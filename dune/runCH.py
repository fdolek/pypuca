import re
import gzip
import time
import uproot
import cloudpickle
import numpy as np
from optparse import OptionParser
from multiprocessing import Process

parser = OptionParser()
parser.add_option('-d', '--dataset', help='dataset', dest='dataset')
(options, args) = parser.parse_args()

start_time = time.time()

#path_name = '/home/furkan/work/tpc/'

binsize = 2000
output = {}
external = uproot.open(options.dataset + '.root')['opdigianaExternal']


def run(xar):

    result_array = np.array([])
    for key in external.allkeys():
        kanal = re.findall("_op(.*?)_waveform", format(key))[0]
        searchResult = re.search(xar, kanal, re.M | re.I)
        if searchResult:
            vector = external[key].values
            # print(vector)
            result_array = np.append(result_array, vector, axis=0)
            # print(xar, result_array.shape)
    eventDump = result_array.reshape(int(result_array.size / binsize), binsize)
    output.update({xar: eventDump})
    print(output)
    with gzip.open(options.dataset + '_' + xar + '.pkl.gz', 'wb') as fout:
        cloudpickle.dump(output, fout)
    return xar


if __name__ == '__main__':

    arapuca1 = ['channel_132', 'channel_133', 'channel_134',
                'channel_135', 'channel_136', 'channel_137',
                'channel_138', 'channel_139', 'channel_140',
                'channel_141', 'channel_142', 'channel_143',
                'channel_264', 'channel_265', 'channel_266',
                'channel_267', 'channel_268', 'channel_269',
                'channel_270', 'channel_271', 'channel_272',
                'channel_273', 'channel_274', 'channel_275', ]

    process = []

    for i in arapuca1:
        proc = Process(target=run, args=(i,))
        process.append(proc)
        proc.start()
    for p in process:
        p.join()

print("--- %.2f seconds ---" % (time.time() - start_time))
