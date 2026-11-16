#!/bin/zsh
# usage: proto/export_pdf.sh deck.pptx  -> deck.pdf (via Keynote)
IN="$(cd "$(dirname "$1")"; pwd)/$(basename "$1")"; OUT="${IN%.pptx}.pdf"
osascript <<OSA
tell application "Keynote"
  set d to open POSIX file "$IN"
  delay 2
  export d to POSIX file "$OUT" as PDF
  close d saving no
end tell
OSA
echo "$OUT"
