
# https://misc.flogisoft.com/bash/tip_colors_and_formatting
function log {
    text=$1
    level=${2:-DEBUG}
    location=${3:-$0}
    
    function format_level_text() {

      function format_keywords() {
          echo "$text" | 
            sed -r 's/(error|fail|exception|critical|no)/\\e[31m\1\\'$BC'/gI' |
            sed -r 's/(warn|abort)/\\e[33m\1\\'$BC'/gI' |
            sed -r 's/(success|ok|yes)/\\e[32m\1\\'$BC'/gI'
      }

      case "$level" in
        TRACE)
          BC='\e[90m' # Dark gray
            text=$(format_keywords);;
        DEBUG)
            BC='\e[37m' # Light Gray
          text=$(format_keywords);;
        INFO)
          BC='\e[36m' # Cyan
          text=$(format_keywords);;
      WARN|WARNING)
          BC='\e[33m';; # Yellow
        ERROR)
          BC='\e[31m';; # Red
        CRITICAL)
          BC='\e[5;31m';; # BLINKING Red
        esac

      echo "$BC[$level] $text\e[0m"
    }

    level_text=$(format_level_text)    
    echo -e "\e[90m[`date +"%Y-%m-%d %H:%M:%S"`] [$location] \e[0m$level_text"
}



# log_status
#  Description : Log on the screen whether or not the last command was succesful.
#     Exit the whole script if last command failed (default).
#  Usage : log_status status [log_location] [DoNotExit]
#     status : the return code of the last command, to be call with $?
#     log_location : [optional] The location of the call of this script, to be printed in the log.
#                    By defaultm this is taken as $0, but it can be wrong if you do not source this file before calling this function
#     do_not_exit : [optional] If not used, exit the whole process in case of fail. If any value, just keep the script running...
#  Example :
#    log_status $?
#    log_status $? path/to/this/script
#    log_status $? path/to/this/script DoNotExit
function log_status {
   if [ $1 -eq 0 ]; then
      log "Success" "INFO" $2
   else
      log "Failed" "ERROR" $2:x
      if [ -z $3 ]; then
         exit 1
      fi
   fi
}



# get
# get a value from the conf files :
# Usage :
# get "key"
function get() {
    # Try first on parameters file :
    (cat "$param" | shyaml get-value $1) 2> /dev/null
    if [ $? -eq 0 ]; then return 0; fi

    # Try first on a potential conf file :
    (cat "$conf" | shyaml get-value $1) 2> /dev/null
    if [ $? -eq 0 ]; then return 0; fi

    # then try on a potential local file :
    (cat $ROOT"/etc/local.yml" | shyaml get-value $1) 2> /dev/null
    if [ $? -eq 0 ]; then return 0; fi

    # Then try on the default :
    cat $ROOT"/etc/default.yml" | shyaml get-value $1
}


# send_email
# Usage : subject="Test" path_tmpfile_email="/tmp/email.txt" send_email
function send_email {
    echo -e "\nEnvironment Variables are :" >> $path_tmpfile_email
    echo "$(printenv)" >> $path_tmpfile_email
    $PYTHON_UTILS_PATH $UTILS_PATH/send_email.py "$subject" "$path_tmpfile_email"
}


# Send and execute query in SQL server
# Usage : query="SELECT 1" query_sql
function query_sql  {
    log "Preparing to execute the query: \n$query" 'TRACE' 'bash_utils/main.sh'
    source /usr/local/share/credentials/AD 
    user="$domain\\$user"
    #log "user=$user ,pass=$pass" #Make sure it’s commented out for security reasons
    $PYTHON_UTILS_PATH $UTILS_PATH/query_sql.py "$query" "$user" "$pass"
    log_status $? "bash_utils/main.sh"
}



# Example :
# hive_query_file="foobar.hql"
# min_size_success=10000 \
# sql_db="PricingBMLStaging" \
# SQLTable="HadoopBMLFooBar"
function hive_to_sql {
    
    filename=$(basename -- "$hive_query_file")
    log "filename=$filename" "TRACE" "bash_utils/main.sh"
    log "SQLTable=$SQLTable" "TRACE" "bash_utils/main.sh"
    tmp_id=$SQLTable"_"$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1) # Haddop tablename followed by random 8 char string

    ###########################################################
    log "SCP the query to the hadoop server..."
    scp $hive_query_file s-shpm@chsxedwhdc001:/tmp/$filename
    log_status $? "bash_utils/main.sh"

    ###########################################################
    cmd="ssh 's-shpm@chsxedwhdc001' 'hive -f /tmp/$filename | gzip --stdout > /tmp/"$tmp_id".tsv.gz'"
    log "Remotely copying from hdfs to distant disk... $cmd" "DEBUG" "bash_utils/main.sh"
    eval "$cmd"
    if [ $? -ne 0 ]; then
        cmd="ssh 's-shpm@chsxedwhdc002' 'hive -f /tmp/$filename | gzip --stdout > /tmp/"$tmp_id".tsv.gz'"
        log "First attempt failed... retrying on different server... $cmd" "DEBUG" "bash_utils/main.sh"
        eval "$cmd"
      log_status $? "bash_utils/main.sh"
    fi

    ###########################################################
    cmd="scp s-shpm@chsxedwhdc001:/tmp/"$tmp_id".tsv.gz /tmp/"$tmp_id".tsv.gz"
    log "Fetching the remote temp .gz file to local... $cmd" "DEBUG" "bash_utils/main.sh"
    eval $cmd
    log_status $? "bash_utils/main.sh"

    ###########################################################
    cmd="ssh 's-shpm@chsxedwhdc001' 'rm -f /tmp/"$tmp_id".tsv.gz'"
    log "To be clean, remotely delete tmp file on distant server... $cmd" "DEBUG" "bash_utils/main.sh"
    eval $cmd
    log_status $? "bash_utils/main.sh"

    ###########################################################
    log "Un-gzipping the tmp file on local disk..." "DEBUG" "bash_utils/main.sh"
    log 'gunzip "/tmp/'$tmp_id'.tsv.gz"' "TRACE" 
    gunzip "/tmp/"$tmp_id".tsv.gz"
    log_status $? "bash_utils/main.sh"

    ###########################################################
    if [ -n "$min_size_success" ]; then
        log "Checking the size of the un-gzipped tempfile on local disk..."
        size=$(stat --printf="%s" "/tmp/"$tmp_id".tsv")
        if (( $size < $min_size_success )); then
            log "Something went wrong in the pipeline. The file is less than $min_size_success Bytes. Aborting..." "ERROR" "bash_utils/main.sh"
            log_status 1 "bash_utils/main.sh"
        else
            log_status 0 "bash_utils/main.sh"
        fi
    fi

    ##########################################################"bash_utils/main.sh"
    log "Replacing NULL values in the code" "DEBUG" "bash_utils/main.sh"
    sed -i 's/Null//gI' "/tmp/"$tmp_id".tsv"
    log_status $? "bash_utils/main.sh"

    ###########################################################
    log "Sending the Shops to SQL Server..." "DEBUG" "bash_utils/main.sh"
    path_mount_folder="/network/sql_server/import_buffer/"$tmp_id".tsv"
    mv "/tmp/"$tmp_id".tsv" $path_mount_folder
    log_status $? "bash_utils/main.sh"

    ##########################################################
    log "Inserting new data into the table..." "DEBUG" "bash_utils/main.sh"
    query="use "$sql_db";
           
TRUNCATE TABLE $SQLTable;

BULK INSERT $SQLTable
FROM '\\\\CHCXSQLARMDM008\\FH_Share_SQL\\import_buffer\\"$tmp_id".tsv'
WITH (FIELDTERMINATOR = '0x09', ROWTERMINATOR = '0x0a');" query_sql
    log_status $? "bash_utils/main.sh" DoNotExit

    ##########################################################
    log "To be clean, deleting file in import_buffer on SQL Server..." "DEBUG" "bash_utils/main.sh"
    rm -rf $path_mount_folder
    log_status $? "bash_utils/main.sh" DoNotExit

}
