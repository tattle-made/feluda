#!/usr/bin/env bash

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
pyinstrument -r speedscope -o speedscope_vid_vec_rep_resnet.$current_time.json -m benchmark.vidvec.video_vec_operator_profile