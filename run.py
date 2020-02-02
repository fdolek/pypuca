import pandas as pd
import os
import numpy as np
import pickle
import argparse
import time

start_time = time.time()

channels = ['ch0', 'ch1', 'ch10', 'ch11', 'ch2', 'ch3', 'ch8', 'ch9']
data_dict = {}
path_name = '/eos/project/f/flic2019/Data/XArapuca/run3/'


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
            Nevent = int(s.size / 2024)
            print('number of event', Nevent)

            arr = s. reshape(Nevent, 2024)
            signal = np.delete(arr, np.s_[0:24], axis=1)
            data_dict.update({channels[i]: signal})
            i += 1
            file_list *= 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory you wish to calculate.', type=str)
    parser.add_argument('-o', '--output', help='Outout restult to a pkl', action='store_true')

    args = parser.parse_args()
    result = pkl(args.dir)
    if result is None:
        print("--- %.2f seconds ---" % (time.time() - start_time))
    else:
        print('test')

    if args.output:

        output = open('myfile.pkl', 'wb')
        pickle.dump(data_dict, output)
        output.close()


if __name__ == '__main__':

    main()
