#!/usr/bin/env bash

./video_vec_operator_time.sh
./video_vec_operator_cprofile.sh
./video_vec_operator_profile_memray.sh
./video_vec_operator_profile_pyinstrument.sh
tail -f /dev/null