#!/usr/bin/bash

# As a reminder, all path should be written in relative from $ROOT :
# ROOT is either passed to main.sh (in case of Framework project) or defined as the location of this file :
ROOT_base=$(dirname $(realpath $0))
if [ -n "$ROOT_suffix" ]; then
    ROOT="$ROOT_base$ROOT_suffix"
else
    ROOT=$ROOT_base
fi

log_folder=$ROOT"/log"
log_file=$log_folder"/"`date +%Y-%m-%d_%H%M%S`".log" 

# Passing these global variable into the param json file, so a R/Python script could access them :
tmp_json_path="/tmp/"$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)".json"
echo '{"ROOT": "'$ROOT'", "log_folder": "'$log_folder'", "log_file": "'$log_file'"}' > $tmp_json_path

# Allowing for passing relative path as conf file :
# If a conf argument is passed but it does not correspond to any absolute path, pass it to relative :
if [ -n "$conf" ] && [ ! -f "$conf" ]; then
     conf=$ROOT"/etc/"$conf
fi

# Create log_folder if needed :
mkdir -p $log_folder
# To avoid the folder to 'explode', delete everything but the last 100 log files :
ls -t "$ROOT/log/" | tail -n +101 | xargs -I% sh -c "rm $ROOT/log/%"

#####################################################################
###### PLEASE CHNAGE THE FOLLOWING DEPENDING ON YOUR SCRIPT #########
#####################################################################

# An example in Bash :
echo -e "########## AN EXAMPLE IN BASH : #######"
source $ROOT/example_in_bash.sh 2>&1 | tee -a $log_file

# An example in Python :
echo -e "\n\n\n########## AN EXAMPLE IN PYTHON : #########"
$ROOT/bin/python "$ROOT/example_in_python.py" "$tmp_json_path" "$conf" 2>&1 | tee -a $log_file

# An example in R :
echo -e "\n\n\n########## AN EXAMPLE IN R : #########"
$ROOT/bin/R "$ROOT/example_in_R.R" "$tmp_json_path" "$conf" 2>&1 | tee -a $log_file
