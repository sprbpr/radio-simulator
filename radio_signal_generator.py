from scipy.io import wavfile as wav
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

ChannelCount = int(input("How many channels do you have? "))  # Get the number of channels
Data = []  # Store all the channels signals in one array
Result = []  # Final radio signals

audio = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16  # Format of sampling 16 bit int
CHANNELS = 1  # Number of channels it means number of sample in every sampling
RATE = 44100  # Number of sample in 1 second sampling
CHUNK = 1024  # Length of every chunk
RECORD_SECONDS = 5  # Time of recording in seconds

# Initialize the Result array
for i in range(RECORD_SECONDS * 44032):
    Result.append(0)

for i in range(ChannelCount):

    input("Press enter to start")  # Start recording when you press enter

    WAVE_OUTPUT_FILENAME = "Channel " + str(i) + ".wav"  # Store each channel with this name

    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    for j in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # storing voice
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    rate, data = wav.read(WAVE_OUTPUT_FILENAME)  # Get data from each wav file which was stored

    # Append each array of data into one array call Data
    for j in range(len(data)):
        Data.append(data[j])

# Shift each channel with different frequencies
for i in range(ChannelCount):
    for j in range(5 * 44032):
        Data[i * (5 * 44032) + j] = Data[i * (RECORD_SECONDS * 44032) + j] * 2 * np.cos(2 * np.pi * i * j / (ChannelCount + 2))

# Add each shifted channel to  Result array
for i in range(ChannelCount):
    for j in range(5 * 44032):
        Result[j] = Result[j] + Data[i * (RECORD_SECONDS * 44032) + j]

# Check how fourier of Result array look like
# It should have 2 * Channel_Count peaks
f = np.fft.fft(Result)
plt.plot(f)
plt.show()

# Write Result array in text file
Radio_Signals = open("Radio Signals.txt", "w+")
for signal in Result:
    Radio_Signals.write(str(signal))
Radio_Signals.close()
