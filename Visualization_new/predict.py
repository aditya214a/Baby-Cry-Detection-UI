import csv, pathlib, librosa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from tensorflow.keras.models import load_model 
import pickle
# from sklearn.preprocessing import StandardScale

class Predict:
    def __init__(self):
        # pass
        self.model = load_model('ff_nn_v_Ac88_Be.h5')
        self.model.load_weights("ff_nn_v_Ac88_Be_weights.h5")

        file = open("scaler_param.obj",'rb')
        self.sc = pickle.load(file)

    def predict(self,name,window):
        # global model
        #Doing prediction
        songname = name+'.wav'
        # for filename in os.listdir(f'b_cry/{g}'):
        # plt.figure(figsize=(8,8))
        # cmap = plt.get_cmap('inferno')
        # pathlib.Path(f'live_data/').mkdir(parents=True, exist_ok=True)
        # y, sr = librosa.load(songname, mono=True, duration=7)
        # plt.specgram(y, NFFT=2048, Fs=2, Fc=0, noverlap=128, cmap=cmap, sides='default', mode='default', scale='dB');
        # plt.axis('off');
        # plt.savefig(f'live_data/{name}.png')
        # plt.clf()


        y, sr = librosa.load(songname, mono=True, duration=5)
        
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)

        header = 'filename '
        for i in range(1, 41):
            header += f' mfcc{i}'
        # header += ' label'
        header = header.split()
        # file = open(f'{name}.csv', 'w', newline='')
        # with file:
        #     writer = csv.writer(file)
        #     writer.writerow(header)

        to_append = f'{name}.wav '
        for e in mfcc:
            to_append += f' {np.mean(e)}'
        # file = open(f'{name}.csv', 'a', newline='')
        # with file:
        #     writer = csv.writer(file)
        #     writer.writerow(to_append.split())
       
        # to_append = [[float(i) for i in to_append]]
        # live_data = pd.read_csv(f'{name}.csv')
        op=list(to_append.split())
        op.pop(0)
        Xnew = self.sc.transform([op])
        ynew = self.model.predict_proba(Xnew)
        # ynew = 1
        print(ynew)
        # ynew = 'The prediction: Crying sound is detected' if ynew[0][0]>ynew[0][1] else 'The prediction: No crying sound is detected'
        if ynew[0][0]>ynew[0][1]:
            # print('Cry')
            y=0
        else:
            # print('No cry')
            y=1
        window.cry_toggle(y)

    def close(self):
        pass
