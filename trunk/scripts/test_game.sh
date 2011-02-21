#!/bin/bash

source setup.sh

javac -help >/dev/null 2>/dev/null
if [ $? -ne 0 ]
then
  echo "Unable to locate java."
  exit 1
fi

echo "=== Minecraft Coder Pack $MCPVERSION ==="

if [ -e "$MCBIN/net/minecraft/client/Minecraft.class" ]
then
  java -Xmx1024M -Xms1024M -cp $MCTESTCP -Djava.library.path="$MCNAT" Start
else
  echo "*** Client not compiled, run recompile.sh"
fi
