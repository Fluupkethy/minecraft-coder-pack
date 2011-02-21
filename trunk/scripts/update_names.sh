#!/bin/bash

source setup.sh

$MCPGETCSV -d "$MCPCONFDIR" 2>/dev/null

if [ $? -ne 0 ]
then
  echo "- Connection timed out, please try again later."
  exit 1;
fi

$MCPRENAMER -R -c "$MCPCONFDIR/renamer.conf"
