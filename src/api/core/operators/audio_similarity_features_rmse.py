import numpy as np
import librosa
from playsound import playsound


def load_file(filename):
    # load file as mono channel at 22050Hz sampling rate: y - waveform, sr - sampling rate
    y, sr = librosa.load(filename)
    return y, sr


def create_features(y, sr):
    # hop length 512 at sr=22050 ~ 23ms
    hop_length = 512

    # Separate harmonics (tonal) and percussive (transient) into separate waveforms
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # Compute Short-Time Fourier Transform (STFT) chromagram
    # Returns: chromagram np.ndarray [shape=(…, n_chroma, t)]
    #  Normalized energy for each chroma bin at each frame.
    chromagram_stft = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=hop_length, n_chroma=12)

    # Compute the first 13 (relevant) MFCC features from raw sample
    # Returns: numpy.ndarray of shape (n_mfcc, T)
    #   T denotes track duration in frames i.e. hop_length
    #   MFCC sequence
    mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)

    # First-order differences (delta features)
    # Output: numpy.ndarray of shape (n_mfcc, T)
    #   T denotes track duration in frames i.e. hop_length
    mfcc_delta = librosa.feature.delta(mfcc)

    # Compute Constant-Q chromagram from only the harmonic (tonal) signal
    # Output:  numpy.ndarray of shape (12, T)
    #   T denotes track duration in frames i.e. hop_length
    chromagram_cqt = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)

    # Compute Spectral Flatness
    # Returns: flatness np.ndarray [shape=(…, 1, t)]
    #   spectral flatness for each frame. The returned value is in [0, 1] and often converted to dB scale.
    spectral_flatness = librosa.feature.spectral_flatness(y=y_harmonic, hop_length=hop_length)

    # Stack all features
    # n_rows: 12+13+13+12+1 = 51
    # Output shape: (51, T)
    audio_features = np.vstack([chromagram_stft, mfcc, mfcc_delta,
                                chromagram_cqt, spectral_flatness])
    # Output shape: (T, 51) - columns should always represent features
    audio_features = audio_features.transpose()
    # print('audio_features.shape:', audio_features.shape)
    return audio_features


def calc_rmse(feat_1, feat_2):
    error = np.subtract(feat_1, feat_2)
    squared_error = np.square(error)
    mse = np.mean(squared_error)
    rmse = np.sqrt(mse)
    return rmse


def calc_similarity_score(ref_features, filename):
    y, sr = load_file(filename)
    audio_features = create_features(y, sr)

    # pad rows to match with mean of feature values in db
    rows_1 = ref_features.shape[0]
    rows_2 = audio_features.shape[0]
    diff_rows = abs(rows_1-rows_2)

    if rows_1 > rows_2:
        count = 0
        while count < diff_rows:
            audio_features = np.insert(audio_features, audio_features.shape[0], ref_mean_padding, axis=0)
            count += 1
    elif rows_2 > rows_1:
        count = 0
        while count < diff_rows:
            ref_features = np.insert(ref_features, ref_features.shape[0], ref_mean_padding, axis=0)
            count += 1

    rmse = calc_rmse(ref_features, audio_features)
    return rmse


# sample file
file1 = librosa.example('nutcracker')
# playsound(file1)
y1, sr1 = load_file(file1)
audio_features1 = create_features(y1, sr1)
ref_mean_padding = np.mean(audio_features1, axis=0)

file2 = librosa.example('humpback')
# playsound(file2)

file3 = librosa.example('brahms')
# playsound(file3)

# assert rmse==0.0 for same file
rmse_score = calc_similarity_score(audio_features1, file1)
print('rmse_score:', rmse_score)
rmse_score = calc_similarity_score(audio_features1, file2)
print('rmse_score:', rmse_score)
rmse_score = calc_similarity_score(audio_features1, file3)
print('rmse_score:', rmse_score)
