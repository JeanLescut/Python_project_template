#!/usr/bin/bash

# As a reminder, all path should be written in relative from $ROOT :
ROOT=$(dirname $(realpath $0))
log_folder=$ROOT"/log"
log_file=$log_folder"/"`date +%Y-%m-%d_%H%M%S`".log" 

# Passing these global variable into the param yaml file, so a R or a Python script could call them :
if [ -z "$param_yaml" ]; then
    param_yaml="/tmp/"$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)".yml"
    touch $param_yaml
fi
echo "ROOT: $ROOT" >> $param_yaml
echo "log_folder: $log_folder" >> $param_yaml
echo "log_file: $log_file" >> $param_yaml

# Allowing for passing relative path as conf file :
# If a conf argument is passed but it does not correspond to any absolute path, pass it to relative :
if [ -n "$conf" ] && [ ! -f "$conf" ]; then
     conf=$ROOT"/etc/"$conf
fi

# If it doesn't exist, create log_folder
mkdir -p $log_folder
# To avoid the folder to 'explode', delete everything but the last 100 log files :
ls -t "$ROOT/log/" | tail -n +101 | xargs -I% sh -c "rm $ROOT/log/%"
# Loading configuration file for the whole
if [ -f "$ROOT/etc/local.sh" ]; then source $ROOT"/etc/local.sh"; fi

#####################################################################
###### PLEASE CHNAGE THE FOLLOWING DEPENDING ON YOUR SCRIPT #########
#####################################################################

# An example in Bash :
echo -e "########## AN EXAMPLE IN BASH : #######"
source $ROOT/example_in_bash.sh 2>&1 | tee -a $log_file

# An example in Python :
echo -e "\n\n\n########## AN EXAMPLE IN PYTHON : #########"
$ROOT/bin/python "$ROOT/example_in_python.py" "$param_yaml" "$conf" 2>&1 | tee -a $log_file

# An example in R :
echo -e "\n\n\n########## AN EXAMPLE IN R : #########"
$ROOT/bin/R "$ROOT/example_in_R.R" "$param_yaml" "$conf" 2>&1 | tee -a $log_file
