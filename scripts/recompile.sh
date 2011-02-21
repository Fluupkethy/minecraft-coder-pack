#!/bin/bash

source setup.sh

javac -help >/dev/null 2>/dev/null
if [ $? -ne 0 ]
then
  echo "Unable to locate javac."
  exit 1
fi

mkdir -p "$MCBIN"
mkdir -p "$MCSBIN"

echo "=== Minecraft Coder Pack $MCPVERSION ===" > "$MCPCOMPLOG"

echo "MCP $MCPVERSION running in $MCPDIR"

if [ -e "$MCJADOUT/net/minecraft/client/Minecraft.java" ]
then
  echo "Compiling Minecraft"
  echo "*** Compiling Minecraft" >> "$MCPCOMPLOG"
  javac -g -verbose -classpath $MCCP -sourcepath "$MCJADOUT" -d "$MCBIN" "$MCSRC1"/*.java "$MCSRC2"/*.java "$MCSTART" "$MCSNDFIX" 2>&1 | tee -a "$MCPCOMPLOG" | grep -v "^\[" | grep -v "^Note:"
else
  if [ -e "$MCJAR" ]
  then
    echo "*** Client not decompiled, run decompile.sh"
  else
    echo "*** minecraft.jar not found, skipping"
  fi
fi

if [ -e "$MCSJADOUT/net/minecraft/server/MinecraftServer.java" ]
then
  echo "Compiling Minecraft Server"
  echo "*** Compiling Minecraft Server" >> "$MCPCOMPLOG"
  javac -g -verbose -sourcepath "$MCSJADOUT" -d "$MCSBIN" "$MCSSRC1"/*.java "$MCSSRC2"/*.java 2>&1 | tee -a "$MCPCOMPLOG" | grep -v "^\[" | grep -v "^Note:"
else
  if [ -e "$MCSJAR" ]
  then
    echo "*** Server not decompiled, run decompile.sh"
  else
    echo "*** minecraft_server.jar not found, skipping"
  fi
fi

echo "=== MCP $MCPVERSION recompile script finished ==="
