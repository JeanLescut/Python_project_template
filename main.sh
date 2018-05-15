#!/usr/bin/bash
ROOT=$(dirname $(realpath $0))
UTILS_PATH=$ROOT/bash_utils
echo '$ROOT='$ROOT
echo '$UTILS_PATH='$UTILS_PATH

log_folder=$ROOT"/log"
export log_file=$log_folder"/"`date +%Y-%m-%d_%H%M%S`".log" # Hopefully partner_pos is not empty

# If it doesn't exist, create log_folder
mkdir -p $log_folder

# To avoid the folder to 'explode', delete everything but the last 100 log files :
ls -t "$ROOT/log/" | tail -n +101 | xargs -I% sh -c "rm $ROOT/log/%"

# Launch script and tee-ing all std to a log file
source $ROOT/pipeline.sh $@ 2>&1 | tee -a $log_file

