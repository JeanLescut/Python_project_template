source $ROOT"/etc/default.sh"
if [ -f "$ROOT/etc/local.sh" ]; then source $ROOT"/etc/local.sh"; fi
if [ -n "$conf" ]; then source $ROOT"/etc/"$conf; fi
source $UTILS_PATH/main.sh

######################################################

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
echo ""
log "Here are the variable loaded : " "TRACE"
declare -p | grep VARIABLE

echo -e "\n\n"
log "PYTHON PART : " "INFO"
$PYTHON_PATH $ROOT/pipeline.py
