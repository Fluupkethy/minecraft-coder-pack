#!/bin/bash

source setup.sh

echo "=== Minecraft Coder Pack $MCPVERSION ===" > "$MCPLOG"

echo "MCP $MCPVERSION running in $MCPDIR"

if [ -e "$MCJAR" ]
then
  if [ -e "$MCJADOUT/net/minecraft/client/Minecraft.java" ]
  then
    echo "*** minecraft.jar already decompiled, run cleanup.sh"
    echo "*** minecraft.jar already decompiled" >> "$MCPLOG"
  else
    echo "*** minecraft.jar was found, processing" >> "$MCPLOG"

    echo "Deobfuscating minecraft.jar"
    echo "*** Deobfuscating $MCJAR" >> "$MCPLOG"
    $MCPRG "$MCJAR" "$MCRGJAR" "$MCRGSCRIPT" "$MCRGLOG" $REINDEX_NUMBER >> "$MCPLOG"

    echo "Unpacking minecraft.jar"
    echo "*** Unpacking $MCJAR" >> "$MCPLOG"
    unzip -o "$MCRGJAR" -d "$MCTEMP" >> "$MCPLOG"
    rm -f "$MCTEMP/META-INF"/MOJANG_C.*
    rm -f "$MCTEMP/null"

    echo "Fixing minecraft classes"
    echo "*** Fixing minecraft classes" >> "$MCPLOG"
    $MCPJR "$MCTEMP" >> "$MCPLOG" 2> /dev/null

    echo "Decompiling minecraft classes"
    echo "*** Decompiling minecraft classes" >> "$MCPLOG"
    $MCPJAD -b -d "$MCJADOUT" -dead -o -r -s .java -stat -v "$MCTEMP"/*.class "$MCTEMP/net/minecraft/client"/*.class 2>> "$MCPLOG"

    echo "Repackage minecraft sources"
    echo "*** Repackage minecraft sources" >> "$MCPLOG"
    $MCPREPACK "$MCJADOUT" "$MCSRC2" >> "$MCPLOG"

    echo "Patching minecraft sources"
    echo "*** Patching minecraft sources" >> "$MCPLOG"
    sed '/^[-+]\{3\} /s/\\/\//g' "$MCPATCH" | patch --binary -p1 -u -d "$MCJADOUT" 2>&1 | tee -a "$MCPLOG" | grep -v "^patching file" | grep -v "Stripping trailing CRs"
  fi
else
  echo "Minecraft.jar was not found."
  echo "Minecraft.jar was not found" >> "$MCPLOG"
fi

if [ -e "$MCSJAR" ]
then
  if [ -e "$MCSJADOUT/net/minecraft/server/MinecraftServer.java" ]
  then
    echo "*** minecraft_server.jar already decompiled, run cleanup.sh"
    echo "*** minecraft_server.jar already decompiled" >> "$MCPLOG"
  else
    echo "*** minecraft_server.jar was found, processing" >> "$MCPLOG"

    echo "Deobfuscating minecraft_server.jar"
    echo "*** Deobfuscating $MCSJAR" >> "$MCPLOG"
    $MCPRG "$MCSJAR" "$MCSRGJAR" "$MCSRGSCRIPT" "$MCSRGLOG" >> "$MCPLOG"

    echo "Unpacking minecraft_server.jar"
    echo "*** Unpacking $MCSJAR" >> "$MCPLOG"
    unzip -o "$MCSRGJAR" -d "$MCSTEMP" >> "$MCPLOG"
    rm -f "$MCSTEMP/null"

    echo "Fixing minecraft server classes"
    echo "*** Fixing minecraft server classes" >> "$MCPLOG"
    $MCPJR "$MCSTEMP" >> "$MCPLOG" 2> /dev/null

    echo "Decompiling minecraft server classes"
    echo "*** Decompiling minecraft server classes" >> $MCPLOG
    $MCPJAD -b -d "$MCSJADOUT" -dead -o -r -s .java -stat -v "$MCSTEMP"/*.class "$MCSTEMP/net/minecraft/server"/*.class 2>> "$MCPLOG"

    echo "Repackage minecraft server sources"
    echo "*** Repackage minecraft server sources" >> "$MCPLOG"
    $MCPREPACK "$MCSJADOUT" "$MCSSRC2" >> "$MCPLOG"

    echo "Patching minecraft server sources"
    echo "*** Patching minecraft server sources" >> "$MCPLOG"
    sed '/^[-+]\{3\} /s/\\/\//g' "$MCSPATCH" | patch --binary -p1 -u -d "$MCSJADOUT" 2>&1 | tee -a "$MCPLOG" | grep -v "^patching file" | grep -v "Stripping trailing CRs"
  fi
else
  echo "Minecraft_server.jar was not found."
  echo "Minecraft_server.jar was not found" >> "$MCPLOG"
fi

if [ -e "$MCPSPLASHES" -a -e "$MCTEMP" ]
then
  cp "$MCPSPLASHES" "$MCSPLASHES"
fi

echo "Renaming methods and fields"
echo "*** Renaming methods and fields" >> "$MCPLOG"
$MCPRENAMER -R -c "$MCPCONFDIR/renamer.conf" >> "$MCPLOG" 2> /dev/null

echo "=== MCP $MCPVERSION decompile script finished ==="
