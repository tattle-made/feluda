from core.models.media_factory import AudioFactory
from core.operators import audio_vec_embedding

# audio_url = "https://github.com/aatmanvaidya/audio-files/blob/main/audio30.wav?raw=true"
# audio_url = "https://github.com/aatmanvaidya/audio-files/blob/main/mp3-sample-audio.mp3"
audio_url = "https://github.com/aatmanvaidya/audio-files/blob/main/ogg-sample-audio.ogg"
new_url = audio_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
dwn = AudioFactory.make_from_url_to_wav(new_url)
print(dwn)
audio_vec_embedding.initialize(param=None)
audio_emb = audio_vec_embedding.run(dwn)
audio_emb_list = audio_emb.tolist()
print(len(audio_emb_list))