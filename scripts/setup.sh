#!/bin/bash

MCPVERSION="2.7"

if [ "`uname`" == "Darwin" ]
then
  OS=osx
else
  OS=linux
fi

MCPDIR=`pwd`

if [ "${0/decompile}" != "$0" -o "$MCPDIR" != "${MCPDIR/ }" ]
then
  echo "=== Creating directory symlink in /tmp..."
  TMPFILE=`mktemp /tmp/mcpXXXXX`
  if ! [ -f "$TMPFILE" ]; then
    echo "=== Could not create temporary file!"
    exit 1
  fi

  ln -sf "`pwd`" "$TMPFILE"
  if ! [ -h "$TMPFILE" ]; then
    echo "=== Could not create directory symlink!"
    rm -f "$TMPFILE"
    exit 1
  fi

  cd "$TMPFILE"
  trap "rm -f $TMPFILE" 0
  MCPDIR="$TMPFILE"
fi

MCPTOOLSDIR="$MCPDIR/tools"
MCPPYTHONTOOLSDIR="$MCPDIR/tools-python"
MCPLOGDIR="$MCPDIR/logs"
MCPJARSDIR="$MCPDIR/jars"
MCPCONFDIR="$MCPDIR/conf"
MCPTEMPDIR="$MCPDIR/temp"
MCPSOURCESDIR="$MCPDIR/sources"
MCPSOURCEBASE="sources"
MCPPATCHDIR="$MCPDIR/patches"
MCPBINDIR="$MCPDIR/bin"
MCPMODDIR="$MCPDIR/mods"
MCPOUTDIR="$MCPDIR/final_out"

MCPLOG="$MCPLOGDIR/minecraft.log"
MCPCOMPLOG="$MCPLOGDIR/minecraft_compile.log"

MCPRG="java -cp $MCPTOOLSDIR/retroguard.jar RetroGuard"
MCPJR="java -jar $MCPTOOLSDIR/jadretro.jar"
if [ $OS == linux ]
then
  MCPJAD="wine $MCPTOOLSDIR/jad.exe"
else
  MCPJAD="$MCPTOOLSDIR/jad-osx"
fi
MCPRENAMER="python $MCPPYTHONTOOLSDIR/renamer_v3.py"
MCPREPACK="$MCPTOOLSDIR/repackage.sh"
MCPOBFUSC="python $MCPPYTHONTOOLSDIR/obfuscathon.py"
MCPGETCSV="python $MCPPYTHONTOOLSDIR/get_csv.py"

MCJAR="$MCPJARSDIR/bin/minecraft.jar"
MCSJAR="$MCPJARSDIR/minecraft_server.jar"
MCJI="$MCPJARSDIR/bin/jinput.jar"
MCJGL="$MCPJARSDIR/bin/lwjgl.jar"
MCJGLU="$MCPJARSDIR/bin/lwjgl_util.jar"
MCCP="$MCJAR:$MCJI:$MCJGL:$MCJGLU"

MCRGJAR="$MCPTEMPDIR/minecraft_rg.jar"
MCRGSCRIPT="$MCPCONFDIR/minecraft.rgs"
MCRGLOG="$MCPLOGDIR/minecraft_rg.log"

MCSRGJAR="$MCPTEMPDIR/minecraft_server_rg.jar"
MCSRGSCRIPT="$MCPCONFDIR/minecraft_server.rgs"
MCSRGLOG="$MCPLOGDIR/minecraft_server_rg.log"

MCTEMP="$MCPTEMPDIR/minecraft"
MCSTEMP="$MCPTEMPDIR/minecraft_server"

MCJADOUT="$MCPSOURCESDIR/minecraft"
MCSJADOUT="$MCPSOURCESDIR/minecraft_server"

MCPACKAGE="net.minecraft.src"
MCSPACKAGE="net.minecraft.src"

MCPATCH="$MCPPATCHDIR/minecraft.patch"
MCSPATCH="$MCPPATCHDIR/minecraft_server.patch"
MCPSPLASHES="$MCPPATCHDIR/splashes.txt"

REINDEX_NUMBER="21000"

MCSTART="$MCPPATCHDIR/Start.java"
MCSNDFIX="$MCPPATCHDIR/gd.java"

MCSRC1="$MCPSOURCEBASE/minecraft/net/minecraft/client"
MCSRC2="$MCPSOURCEBASE/minecraft/net/minecraft/src"
MCBIN="$MCPBINDIR/minecraft"
MCSSRC1="$MCPSOURCEBASE/minecraft_server/net/minecraft/server"
MCSSRC2="$MCPSOURCEBASE/minecraft_server/net/minecraft/src"
MCSBIN="$MCPBINDIR/minecraft_server"

MCSPLASHES="$MCTEMP/title/splashes.txt"

MCTESTCP="$MCBIN:$MCTEMP:$MCJI:$MCJGL:$MCJGLU"
MCNAT="$MCPJARSDIR/bin/natives"
MCSTESTCP="$MCSBIN:$MCSTEMP"

MCREOBSCRIPT="$MCPDIR/conf/minecraft_rev.saffx"
MCSREOBSCRIPT="$MCPDIR/conf/minecraft_server_rev.saffx"
MCREOBDIR="$MCPOUTDIR/minecraft"
MCSREOBDIR="$MCPOUTDIR/minecraft_server"

MCPREOBLOG="$MCPDIR/logs/reobf.log"
MCREOBLOG="$MCPDIR/logs/reobf_minecraft_rg.log"
MCSREOBLOG="$MCPDIR/logs/reobf_minecraft_server_rg.log"

MODCOMPLOG="$MCPLOGDIR/mcpmod_compile.log"
MODTEMP="$MCBIN"
MODREOBDIR="$MCPTEMPDIR/mods"
MODSOURCEBASE="mods/MCP"
MODCP="$MCPMODDIR/mcp_v1.jar:$MCTESTCP"
MODJAR="$MCPOUTDIR/mcp_12_02.jar"

if [ "$1" == --init ] || [ ! -e "$MCPCONFDIR/init" ]
then
  echo "=== Initializing MCP $MCPVERSION environment ==="

  echo "+++ Checking scripts"
  chmod +x "$MCPDIR"/*.sh
  chmod +x "$MCPTOOLSDIR"/*.sh
  chmod +x "$MCPTOOLSDIR"/jad-*

  echo "+++ Checking directory structure"
  echo "+ $MCPOUTDIR"
  mkdir -p "$MCPOUTDIR"

  echo "+ $MCPJARSDIR"
  mkdir -p "$MCPJARSDIR"

  echo "+ $MCPLOGDIR"
  mkdir -p "$MCPLOGDIR"

  echo "+ $MCPSOURCESDIR"
  mkdir -p "$MCPSOURCESDIR"

  echo "+ $MCPTEMPDIR"
  mkdir -p "$MCPTEMPDIR"

  touch "$MCPCONFDIR/init"

  echo "=== MCP $MCPVERSION initialized. ==="
fi
