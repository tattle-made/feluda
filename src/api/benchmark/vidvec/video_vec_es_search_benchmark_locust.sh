#!/usr/bin/env bash

python -m benchmark.vidvec.video_vec_es_indexer
locust -f benchmark/vidvec/video_vec_es_search_benchmark_locust.py --headless -u 1000 -r 10 --run-time 2m --stop-timeout 30s --csv vid_vec_es_search_locust