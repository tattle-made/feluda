#!/usr/bin/env bash

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
python -m memray run -o image_vec_rep_resnet.$current_time.bin -m benchmark.imgvec.image_vec_operator_profile