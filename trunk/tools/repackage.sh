#!/bin/bash

sed -e '/\/\/ Decompiled by Jad/i\
package net.minecraft.src;' -i.old "$1"/*.java

mkdir -p "$2" 2>/dev/null
mv -f -v "$1"/*.java "$2" 2>/dev/null
rm "$1"/*.old 2>/dev/null
