#!/bin/bash

source setup.sh

rm -rf "$MCREOBDIR" 2>/dev/null
rm -rf "$MCSREOBDIR" 2>/dev/null
mkdir -p "$MCREOBDIR"
mkdir -p "$MCSREOBDIR"

echo "=== Minecraft Coder Pack $MCPVERSION ===" > "$MCPREOBLOG"

echo "MCP $MCPVERSION running in $MCPDIR"
if [ -e "$MCBIN/net/minecraft/client/Minecraft.class" ]
then
  echo "+ Obfuscating client:"
  echo "+ Obfuscating client." >> "$MCPREOBLOG"
  $MCPOBFUSC -c "$MCPCONFDIR/client_obfuscation.txt" -d "$MCREOBSCRIPT" -i "$MCBIN" -o "$MCREOBDIR" >> "$MCPREOBLOG" 2>&1
  if [ $? -eq 1 ]
  then
    echo "## CLIENT OBFUSCATION FAILED ##"
    echo "See $MCPREOBLOG for detailed information!"
    exit 1
  fi
else
  echo "*** Client not compiled, skipping"
fi

if [ -e "$MCSBIN/net/minecraft/server/MinecraftServer.class" ]
then
  echo "+ Obfuscating server:"
  echo "+ Obfuscating server." >> "$MCPREOBLOG"
  $MCPOBFUSC -c "$MCPCONFDIR/server_obfuscation.txt" -d "$MCSREOBSCRIPT" -i "$MCSBIN" -o "$MCSREOBDIR" >> "$MCPREOBLOG" 2>&1
  if [ $? -eq 1 ]
  then
    echo "## SERVER OBFUSCATION FAILED ##"
    echo "See $MCPREOBLOG for detailed information!"
    exit 1
  fi
else
  echo "*** Server not compiled, skipping"
fi

echo "=== MCP $MCPVERSION reobfuscation script finished ==="
