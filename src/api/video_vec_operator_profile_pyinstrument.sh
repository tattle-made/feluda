#! /bin/bash
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
pyinstrument -r speedscope -o speedscope_vid_vec_rep_resnet.$current_time.json video_vec_operator_profile.py
tail -f /dev/null