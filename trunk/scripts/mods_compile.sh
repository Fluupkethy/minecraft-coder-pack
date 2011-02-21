#!/bin/bash

source setup.sh

javac -help >/dev/null 2>/dev/null
if [ $? -ne 0 ]
then
  echo "Unable to locate javac."
  exit 1
fi

mkdir -p "$MODREOBDIR"

echo "=== Minecraft Coder Pack $MCPVERSION ===" > "$MODCOMPLOG"

echo "MCP $MCPVERSION running in $MCPDIR"

if [ -e "$MCBIN/net/minecraft/client/Minecraft.class" ]
then
  echo "Compiling MCP Mod Launcher"
  echo "*** Compiling MCP Mod Launcher" >> "$MCPCOMPLOG"
  for a in "$MODSOURCEBASE"/*
  do
    javac -g -verbose -classpath $MODCP -sourcepath "$MCPMODDIR" -d "$MODTEMP" "$a"/*.java 2>&1 | tee -a "$MODCOMPLOG" | grep -v "^\[" | grep -v "^Note:"
  done

  cd "$MODTEMP"
  jar xf "$MCPMODDIR/mcp_v1.jar"
  rm -rf META-INF
  cd "$MCP"

  if [ -e "$MODTEMP/MCP/Mod.class" ]
  then
    echo "+ Obfuscating mods."
    echo "+ Obfuscating mods." >> "$MODCOMPLOG"
    $MCPOBFUSC -c "$MCPCONFDIR/reob.conf" -d "$MCREOBSCRIPT" -i "$MODTEMP" -o "$MODREOBDIR" >> "$MODCOMPLOG"
  else
    echo "*** Mods not compiled, skipping"
  fi

  cp -r "$MCPMODDIR/MCP/mod_jumpblock/lang" "$MODREOBDIR/MCP/mod_jumpblock/"
  cp -r "$MCPMODDIR/MCP/mod_mcp/lang" "$MODREOBDIR/MCP/mod_mcp/"
  cp -r "$MCPMODDIR/MCP/mod_mcp/gfx" "$MODREOBDIR/MCP/mod_mcp/"
  jar cfe "$MODJAR" MCP.Start -C "$MODREOBDIR" .
else
  if [ -e "$MCJADOUT/net/minecraft/client/Minecraft.java" ]
  then
    echo "*** Client not recompiled, run recompile.sh"
  else
    if [ -e "$MCJAR" ]
    then
      echo "*** Client not decompiled, run decompile.sh"
    else
      echo "*** minecraft.jar not found, skipping"
    fi
  fi
fi

echo "=== MCP $MCPVERSION compile mods script finished ==="
