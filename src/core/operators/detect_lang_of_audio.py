"""
This operator uses OpenAI's whisper to detect spoken language in audio files.

pip install :
openai-whisper==20231117
pydub==0.25.1
torch==2.3.0
torchaudio==2.3.0
"""

LANGUAGES = {
    "en": "english",
    "zh": "chinese",
    "de": "german",
    "es": "spanish",
    "ru": "russian",
    "ko": "korean",
    "fr": "french",
    "ja": "japanese",
    "pt": "portuguese",
    "tr": "turkish",
    "pl": "polish",
    "ca": "catalan",
    "nl": "dutch",
    "ar": "arabic",
    "sv": "swedish",
    "it": "italian",
    "id": "indonesian",
    "hi": "hindi",
    "fi": "finnish",
    "vi": "vietnamese",
    "he": "hebrew",
    "uk": "ukrainian",
    "el": "greek",
    "ms": "malay",
    "cs": "czech",
    "ro": "romanian",
    "da": "danish",
    "hu": "hungarian",
    "ta": "tamil",
    "no": "norwegian",
    "th": "thai",
    "ur": "urdu",
    "hr": "croatian",
    "bg": "bulgarian",
    "lt": "lithuanian",
    "la": "latin",
    "mi": "maori",
    "ml": "malayalam",
    "cy": "welsh",
    "sk": "slovak",
    "te": "telugu",
    "fa": "persian",
    "lv": "latvian",
    "bn": "bengali",
    "sr": "serbian",
    "az": "azerbaijani",
    "sl": "slovenian",
    "kn": "kannada",
    "et": "estonian",
    "mk": "macedonian",
    "br": "breton",
    "eu": "basque",
    "is": "icelandic",
    "hy": "armenian",
    "ne": "nepali",
    "mn": "mongolian",
    "bs": "bosnian",
    "kk": "kazakh",
    "sq": "albanian",
    "sw": "swahili",
    "gl": "galician",
    "mr": "marathi",
    "pa": "punjabi",
    "si": "sinhala",
    "km": "khmer",
    "sn": "shona",
    "yo": "yoruba",
    "so": "somali",
    "af": "afrikaans",
    "oc": "occitan",
    "ka": "georgian",
    "be": "belarusian",
    "tg": "tajik",
    "sd": "sindhi",
    "gu": "gujarati",
    "am": "amharic",
    "yi": "yiddish",
    "lo": "lao",
    "uz": "uzbek",
    "fo": "faroese",
    "ht": "haitian creole",
    "ps": "pashto",
    "tk": "turkmen",
    "nn": "nynorsk",
    "mt": "maltese",
    "sa": "sanskrit",
    "lb": "luxembourgish",
    "my": "myanmar",
    "bo": "tibetan",
    "tl": "tagalog",
    "mg": "malagasy",
    "as": "assamese",
    "tt": "tatar",
    "haw": "hawaiian",
    "ln": "lingala",
    "ha": "hausa",
    "ba": "bashkir",
    "jw": "javanese",
    "su": "sundanese",
    "yue": "cantonese",
}

def extract_speech(fname):
    """Detect and export voice activity from an audio file.

    Args:
        fname (str): Path to audio file.

    Returns:
        str or bool: Name of the audio file with the extracted speech, False if no voice activity detected.
    """
    # get speech timestamps using our VAD model...
    get_speech_timestamps, _, read_audio, *_ = utils
    audio = read_audio(fname, sampling_rate=16000)
    speech_timestamps = get_speech_timestamps(
        audio, vad, sampling_rate=16000, return_seconds=True
    )

    # return false if no speech detected:
    if not speech_timestamps:
        return False

    # merge timestamps that are closer than a second for leniency...
    merged_timestamps = []
    current_segment = speech_timestamps[0]
    for next_segment in speech_timestamps[1:]:
        if next_segment['start'] - current_segment['end'] <= 1:
            current_segment['end'] = next_segment['end']
        else:
            merged_timestamps.append(current_segment)
            current_segment = next_segment
    merged_timestamps.append(current_segment)

    # isolate the speech as audio...
    with open(fname, 'rb') as file:
        global audio_segment
        audio_segment = AudioSegment.from_file(file, format="wav")
    segments = []
    duration = 0
    for ts in merged_timestamps:
        start = ts["start"] * 1000
        end = ts["end"] * 1000
        segment = audio_segment[start:end]
        segments.append(audio_segment[start:end])
        duration += len(segment)
        if duration > 30000:
            # exit the loop if we have an audio atleast 30 seconds long
            break
    final_audio = sum(segments, AudioSegment.empty())

    # Export audio as a tmp file...
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as speech:
        final_audio.export(speech.name, format="wav")
    return speech.name

def detect_language(fname):
    """Detect language of from an audio file using whisper.

    Returns:
        str: Detected ISO 639-1 language code.
    """
    # load and normalize audio to fit 30 seconds duration
    audio = whisper.load_audio(fname)
    audio = whisper.pad_or_trim(audio)

    # create log-Mel spectrogram
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect language
    _, probs = model.detect_language(mel)
    return max(probs, key=probs.get)

def initialize(param):
    global whisper, model, AudioSegment, utils, vad, os, tempfile

    import os
    import tempfile
    import whisper
    import torch
    from pydub import AudioSegment

    model = whisper.load_model("base")
    vad, utils = torch.hub.load(repo_or_dir="snakers4/silero-vad", model="silero_vad")

def run(audio_file):
    audio = audio_file["path"]
    speech = extract_speech(audio)
    if speech:
        # audio contains voice activity
        try:
            language_id = detect_language(speech)
            language = LANGUAGES[language_id] # get the generic name from id
            return {"id": language_id, "language": language}
        finally:
            os.remove(speech)
    return {"id": "und", "language": "undefined"}