import numpy as np
import logging
from scipy import signal
from scipy.io import wavfile
from scipy.spatial import distance
# import matplotlib.pyplot as plt
from pydub import AudioSegment
import os

log = logging.getLogger(__name__)

def convert(infile):
    """convert mp3 to wav
    Param: infile(str): a mp3 file, like "music.mp3"
    Export: outfile: a wav file with the same name, like "music.wav"
    """
    try:
        # format outfile name
        filename = os.path.basename(infile)
        outdir = os.path.dirname(infile)
        outfile = os.path.join(outdir, filename[:-3] + "wav")
        # export wav
        sound = AudioSegment.from_mp3(infile)
        sound.export(outfile, format="wav")
    except OSError:
        log.Error("expected an mp3 file in the directory")

def spectrogram(pathfile):
    """read a wav file and return its spectrogram"""
    if not pathfile.endswith(".wav"):
        log.error("audio file must be in wav format")
    else:
        framerate, series = wavfile.read(pathfile)
        log.info("wav file processed")
        # series[:,0] -> left channel
        # series[:,1] -> right channel
        # take mean to get one-channel series
        series = np.mean(series, axis=1)
        log.info("series converted to one-channel")

        f, t, spect = signal.spectrogram(
            series,
            fs=framerate,
            nperseg=10*framerate,
            noverlap=(10-1)*framerate,
            window="hamming"
        )
        log.info("spectrogram computed")

        return framerate, f, t, spect
    
def fingerprint(f, spect):
    """compute fingerprint (ver.1) from spectrogram

    Option 4 in the instruction:
    find a list of (positive) frequencies f (scaled to [0, 1])
    at which the local periodogram has a peak
    """
    max_f = max(f)
    peaks = np.argmax(spect, axis=0)
    fingerprints = f[peaks] / max_f
    log.info("fingerprint (ver.1) computed")

    return np.array(fingerprints)

def fingerprint2(f, spect, framerate):
    """compute fingerprint (ver.2) from spectrogram

    Option 5 in the instruction:
    find the maximum power per octave in local periodograms
    """
    # m = number of octaves
    # must have m>5 to cover middleC
    # larger m -> better precision
    m = 8
    min_f = int((2**-(m+1))*(framerate/2))
    fingerprints = []

    log.info("start to iterate through the spectrogram")

    # iterate through all octaves
    for k in range(m):
        start = min_f*(2**k)*10
        end = min_f*(2**(k+1))*10
        # take subset of spectrogram, slice each octave
        sub_f = f[start:end]
        sub_spect = spect[start:end]
        # compute fingerprint of each subset
        sub_fingerprint = fingerprint(sub_f, sub_spect)
        fingerprints.append(sub_fingerprint)
    # transpose to get fingerprint for each window
    fingerprints = np.array(fingerprints).T

    log.info("fingerprint (ver.2) computed")

    return fingerprints
    
if __name__ == "__main__":
    convert(r'sample_data/audio.mp3')
    audio_file = r'sample_data/audio.wav'
    framerate_v, f_v, t_v, spect_v = spectrogram(audio_file)
    # print('Frame rate - ', framerate_v, 'F - ', f_v, 'T - ', t_v, 'spect - ', spect_v)
    fingerprint_v = fingerprint(f_v, spect_v)
    print('Fingerprint - ', fingerprint_v)
    fingerprint2_v = fingerprint2(f_v, spect_v, framerate_v)
    print('Fingerprint2 - ', fingerprint2_v)

