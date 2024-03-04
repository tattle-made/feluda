#!/usr/bin/env bash

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
python -m memray run -o audio_vec_embedding.$current_time.bin -m benchmark.audiovec.audio_vec_operator_profile