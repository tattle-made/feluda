#!/usr/bin/env bash

./video_vec_operator_time.sh
echo "test 1 done"
./video_vec_operator_cprofile.sh
echo "test 2 done"
./video_vec_operator_profile_memray.sh
echo "test 3 done"
./video_vec_operator_profile_pyinstrument.sh
echo "test 4 done"
./video_vec_operator_timeLoop.sh
echo "test 5 done"
./video_vec_operator_timeMultiple.sh
echo "test 6 done"
tail -f /dev/null