STYLUS_ID="ELAN9004:00 04F3:299E stylus"
TOUCH_ID="ELAN9004:00 04F3:299E"

xinput test -proximity "$STYLUS_ID" |
    while read line; do
        if [[ $line == *out* ]]; then
            xinput enable "$TOUCH_ID";
            echo "Pen lifted"
            sleep 0.5s
        else
            xinput disable "$TOUCH_ID"
            echo "Pen nearby"
        fi
    done
