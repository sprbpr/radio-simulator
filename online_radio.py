from scipy.io import wavfile as wav
import threading
from scipy import signal
import numpy as np
import winsound


# Sample count per second
SampleCount = 480000

# Get the frequency of your wanted channel
ChannelFrequency = int(input("Enter Your Channel Frequency: "))

# Design Blackman Filter
wc = 0.01
dw = 0.01
m = int(np.ceil((12 * np.pi) / (2 * np.pi * dw))) + 1
if m % 2 == 0:
    m = m + 1
w = signal.blackman(m)
n = np.arange(m)
f = np.sinc(2 * wc * (n - (m - 1) / 2.0))
fw = f * w
fw = fw / np.sum(fw)

# Read input.txt and append to listOfLines array
listOfLines = []
with open("input.txt", "r") as myFile:
    for line in myFile:
        listOfLines.append(line.strip())

# Convert listOfLines to data array because we can't use listOfLines as array
temp = np.fft.fft(listOfLines)
Data = np.fft.ifft(temp)

for i in range(10):

    # Shift all channels as much as (2 * np.pi * n * ChannelFrequency / SampleCount)
    # to change our channel's frequency to zero
    ShiftedData = []
    for n in range(480_000 * i, 480_000 * (i + 1)):
        ShiftedData.append(Data[n] * 2 * (np.cos(2 * np.pi * n * ChannelFrequency / SampleCount)))

    # Filter all channels except our chosen channel
    FilteredData = np.convolve(ShiftedData, fw, "same")
    ShiftedData.clear()

    # Make our chosen channel as wav file
    wav.write("Radio.wav", 441000, FilteredData.astype(np.int16))

    # Play chosen channel without click on wav file by python by thread
    Thread = threading.Thread(winsound.PlaySound('Radio.wav', winsound.SND_FILENAME), args=(10,))
    Thread.start()
