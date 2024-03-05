#!/usr/bin/env bash

python -m benchmark.audiovec.audio_vec_operator_multicore > output_multicore.txt
tail -f /dev/null