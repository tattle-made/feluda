#!/usr/bin/env bash

benchmark/video_vec_operator_time.sh
echo "test 1 done"
benchmark/video_vec_operator_cprofile.sh
echo "test 2 done"
benchmark/video_vec_operator_profile_memray.sh
echo "test 3 done"
benchmark/video_vec_operator_profile_pyinstrument.sh
echo "test 4 done"
tail -f /dev/null