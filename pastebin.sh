#! /usr/bin/env bash

shopt -s extglob

PASTEBIN_API="http://pastebin.com/api_public.php"

PASTEBIN_SH=$(basename "$0")
PASTEBIN_FULL_SH="$0"

oneline_usage="$PASTEBIN_SH [-ch] [-f filename]"

usage() {
    echo "Usage: $oneline_usage"
    echo 
    echo "   -c  First copy the text to be posted to pastebin to the local pasteboard."
    echo 
    echo "   -f  Read from FILE instead of STDIN."
    echo 
    echo "   -h  Print this help message."
    exit 1
}

while getopts ":cf:h" Option
do
    case $Option in
        c )
            PASTEBIN_COPY=1
            ;;
        f )
            PASTEBIN_FILE=$OPTARG
            ;;
        h )
            usage
            ;;
    esac
done
shift $((OPTIND - 1))

PASTEBIN_FILE=${PASTEBIN_FILE:-/dev/stdin}
PASTEBIN_COPY=${PASTEBIN_COPY:-0}

PASTEBIN_TO_PASTE="paste_code=`cat $PASTEBIN_FILE`"

if [ $PASTEBIN_COPY = 1 ]; then
    echo "$PASTEBIN_TO_PASTE" | pbcopy
    sleep .5
fi

curl -s -X POST -d "$PASTEBIN_TO_PASTE" $PASTEBIN_API | pbcopy

