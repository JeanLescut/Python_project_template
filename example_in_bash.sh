UTILS_PATH=$ROOT/bash_utils
source $UTILS_PATH/main.sh

#####################################################
# Modify anything below this line : This is your script :
######################################################

log "----------- TESTING LOGGING ----------" "INFO"
log "testing log in TRACE level : the color is quite faded..." "TRACE"
log "testing log in DEBUG level : This is a bit more visible..." "DEBUG"
log "testing log in INFO level : This is clearly visible, and help structuring the logs visually" "INFO"
echo ""
log "testing syntax highlighting : SUCceSs, yes, no, warn, YES, non-important text, critical, Abort, error, end of the test." "TRACE"
log "testing syntax highlighting : SUCceSs, yes, no, warn, YES, non-important text, critical, Abort, error, end of the test." "DEBUG"
log "testing syntax highlighting : SUCceSs, yes, no, warn, YES, non-important text, critical, Abort, error, end of the test." "INFO"
log "testing syntax highlighting : SUCceSs, yes, no, warn, YES, non-important text, critical, Abort, error, end of the test." "WARN"
log "testing syntax highlighting : SUCceSs, yes, no, warn, YES, non-important text, critical, Abort, error, end of the test." "ERROR"
log "testing syntax highlighting : SUCceSs, yes, no, warn, YES, non-important text, critical, Abort, error, end of the test." "CRITICAL"
log "testing syntax highlighting : SUCceSs, yes, no, warn, YES, non-important text, critical, Abort, error, end of the test." "Foobar!"



echo -e "\n"
log "----------- TESTING VARIABLES ---------" "INFO"
name=$(get "name")
log "name=$name" "DEBUG"


