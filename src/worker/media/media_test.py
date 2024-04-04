# from core.models.media_factory import AudioFactory
# from core.operators import audio_vec_embedding

# audio_url = "https://github.com/aatmanvaidya/audio-files/blob/main/audio30.wav"
# audio_url = "https://github.com/aatmanvaidya/audio-files/blob/main/mp3-sample-audio.mp3"
# audio_url = "https://github.com/aatmanvaidya/audio-files/blob/main/ogg-sample-audio.ogg"
# new_url = audio_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
# print(new_url)
# dwn = AudioFactory.make_from_url_to_wav(new_url)
# print(dwn)
# audio_vec_embedding.initialize(param=None)
# audio_emb = audio_vec_embedding.run(dwn)
# audio_emb_list = audio_emb.tolist()
# print(len(audio_emb_list))

# from core.models.media_factory import VideoFactory, AudioFactory
# from core.operators import vid_vec_rep_resnet
# video_url = "https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/sample-cat-video.mp4"
# video_key = "temp/video-01.mp4"
# path = VideoFactory.make_from_url(video_key)
# print(path)
# vid_vec_rep_resnet.initialize(param=None)
# vid_vec = vid_vec_rep_resnet.run(path)
# print(len(list(vid_vec)[0].get('vid_vec')))

from core.models.media_factory import AudioFactory
from core.operators import audio_vec_embedding
audio_url = "https://github.com/aatmanvaidya/audio-files/blob/main/audio30.wav"
new_url = audio_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
audio_key = "temp/audio-01.wav"
path = AudioFactory.make_from_url(audio_key)
print(path)
audio_vec_embedding.initialize(param=None)
audio_emb = audio_vec_embedding.run(path)
audio_emb_list = audio_emb.tolist()
print(len(audio_emb_list))
