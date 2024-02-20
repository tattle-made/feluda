#!/usr/bin/env bash

python -m benchmark.vidvec.video_vec_operator_multicore > output_multicore.txt
tail -f /dev/null