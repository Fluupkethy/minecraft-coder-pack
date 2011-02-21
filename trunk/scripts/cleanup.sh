#!/bin/bash

source setup.sh

USER=`whoami`
if [ "$USER" == "root" ]
then
  echo "=== Don't run cleanup as root! Aborting. ==="
  exit 1
fi

echo "CLEANING UP"

if [ -n "$MCPLOGDIR" ]
then
  rm -f "$MCPLOGDIR"/*.log
  echo "+ $MCPLOGDIR"
fi

if [ -n "$MCPTEMPDIR" ]
then
  rm -f "$MCPTEMPDIR"/*.jar
  rm -f "$MCPTEMPDIR"/*.md5
  echo "+ $MCPTEMPDIR"
fi

if [ -n "$MCBIN" ]
then
  rm -rf "$MCBIN"
  echo "+ $MCBIN"
fi

if [ -n "$MCJADOUT" ]
then
  rm -rf "$MCJADOUT"
  echo "+ $MCJADOUT"
fi

if [ -n "$MCTEMP" ]
then
  rm -rf "$MCTEMP"
  echo "+ $MCTEMP"
fi

if [ -n "$MCPBINDIR" ]
then
  rm -f "$MCPBINDIR"/*.log
  rm -f "$MCPBINDIR"/*.txt
  rm -rf "$MCPBINDIR/world"
  echo "+ $MCPBINDIR"
fi

if [ -n "$MCSBIN" ]
then
  rm -rf "$MCSBIN"
  echo "+ $MCSBIN"
fi

if [ -n "$MCSJADOUT" ]
then
  rm -rf "$MCSJADOUT"
  echo "+ $MCSJADOUT"
fi

if [ -n "$MCSTEMP" ]
then
  rm -rf "$MCSTEMP"
  echo "+ $MCSTEMP"
fi

if [ -n "$MCREOBSCRIPT" ]
then
  rm -f "$MCREOBSCRIPT"
  echo "+ $MCREOBSCRIPT"
fi

if [ -n "$MCSREOBSCRIPT" ]
then
  rm -f "$MCSREOBSCRIPT"
  echo "+ $MCSREOBSCRIPT"
fi

if [ -n "$MODREOBDIR" ]
then
  rm -rf "$MODREOBDIR"
  echo "+ $MODREOBDIR"
fi

if [ -n "$MCPOUTDIR" ]
then
  rm -rf "$MCPOUTDIR/minecraft"
  rm -rf "$MCPOUTDIR/minecraft_server"
  rm -f "$MCPOUTDIR"/*.jar
  echo "+ $MCPOUTDIR"
fi

echo "DONE"
