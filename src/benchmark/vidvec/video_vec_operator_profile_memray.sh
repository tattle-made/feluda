#!/usr/bin/env bash

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
python -m memray run -o vid_vec_rep_resnet.$current_time.bin -m benchmark.vidvec.video_vec_operator_profile