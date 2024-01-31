import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt


def FFT(x):
    N = len(x)

    if N == 1:
        return x
    else:
        X_even = FFT(x[::2])
        X_odd = FFT(x[1::2])
        factor = np.exp(-2j * np.pi * np.arange(N) / N)
        X = np.concatenate([X_even+factor[:int(N/2)]*X_odd,X_even+factor[int(N/2):]*X_odd])
        return X

CHUNK = 1024*4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 10000

p = pyaudio.PyAudio()


stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

data = stream.read(CHUNK)
data_int = np.array(struct.unpack(str(2*CHUNK) + "B", data)).astype(dtype='b')[::2]
fig, (ax,freq,hist) = plt.subplots(nrows=3)
ax.set_ylim(-200,200)
ax.set_xlim(0,CHUNK)
freq.set_xlim(0,CHUNK)
freq.set_ylim(0,10)

hist.set_xlim(0,11)
hist.set_ylim(0,50)

x = np.arange(0,2 * CHUNK, 2)
line, = ax.plot(x,np.random.rand(CHUNK),'-', lw =1)

freq_line, = freq.plot(x,np.random.rand(CHUNK),'-', lw=1)

hist_line, = hist.plot(np.arange(0,11), np.random.rand(11),'-', lw=1)

fig.show()
count = 0
while True:


    data = stream.read(CHUNK)
    data_int = np.array(struct.unpack(str(2 * CHUNK) + "B", data)).astype(dtype='b')[::2]
    line.set_ydata(data_int)

    if (count == 5):
        data_freq = FFT(data_int)
        data_freq = data_freq / len(data_freq)
        freq_line.set_ydata(abs(data_freq[0:CHUNK]))
        hist_data = [0,0,0,0,0,0,0,0,0,0,0]
        for i in range(len(data_freq)):
            hist_data[i//(len(data_freq) // 10)] += data_freq[i]
        hist_line.set_ydata(hist_data)
        count = 0

    fig.canvas.draw()
    fig.canvas.flush_events()
    count += 1



