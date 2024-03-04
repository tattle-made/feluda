#!/usr/bin/env bash

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
pyinstrument -r speedscope -o speedscope_audio_vec_embedding.$current_time.json -m benchmark.audiovec.audio_vec_operator_profile