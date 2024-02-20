#!/usr/bin/env bash

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
pyinstrument -r speedscope -o speedscope_image_vec_rep_resnet.$current_time.json -m benchmark.imgvec.image_vec_operator_profile