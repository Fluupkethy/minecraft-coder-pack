# Minecraft mod creator pack 2.8 for Minecraft 1.2\_02 #

## Prerequisites: ##

  1. Install Java SDK Standard Edition (short JDK).
> > Link: http://www.oracle.com/technetwork/java/javase/downloads/
  1. Add the paths to your JDK and JRE bin folders to the Environment Variable PATH.

```
    Example for Windows users of what you have to add to the variable (entries are seperated by ; )
    C:\Program Files\Java\jdk1.6.0_23\bin;C:\Program Files\Java\jre6\bin

     TODO: need to added instructions for linux and mac
```

## How to use: ##

  1. Prepare the files:
    * Copy the "minecraft\_server.jar" file into the "jars" folder.
    * Copy the folders "bin" and "resources" from your "%APPDATA$\.minecraft" folder into the "jars" folder.
  1. Decompilation and patching
    * Start the "decompile.bat" script in this folder.
  1. Modding
    * Modify the sourcecode in the "sources\minecraft" folder or in the "sources\minecraft\_server" folder.
  1. Compile
    * Start the "recompile.bat" script in this folder.
  1. Testing
    * To test the modified game, start the "test\_game.bat" script
    * To test the modified server, start the "test\_server.bat" script
  1. Obfuscation
    * Decompile the code, modify and recompile.
    * Open "conf\server\_obfuscation.txt" and "conf\client\_obfuscation.txt".
    * Put the name of the classes you want to be obfuscated, one per line. If you create            new classes, they have to be specified as well.
      * The name of the classes are the clear ones (Block, BlockDoor, etc).
      * One example would be :
      * BlockDoor
      * Block
      * Entity
      * ChunkProviderGenerate
      * MyNewAwesomeClass
    * Start "reobf.bat" to start the reobfuscation step.
    * Your obfuscated classes are now available in "final\_out\minecraft" and "final\_out\minecraft\_server", ready to be injected in MC.
    * Make sure to delete the META-INF folder in minecraft.jar, otherwise the game will just black-screen when you start it.
    * BETA FEATURE : For those willing to experiment, a beta GUI is available in the tool directory. It is called obfuscathonCharmer. Just run it, experiment and give us some feedback on it. The GUI is made in C# and should work on both linux and windows (using mono on linux).


## WARNINGS: ##

  * Make sure that you backup the modified sources before you run "decompile.bat" again or all changes will be lost!
  * The "cleanup.bat" file will delete most of the generated files and sources. Be careful with this one :)

## Notes: ##

  * Do not use this to release complete packages of minecraft jar, class or java files. They are copyrighted

> material by Notch and mods should only contain small changes to some classes, never complete sets that
> can be used by people who did not buy the game to play it.

**Make sure you use the original minecraft.jar and minecraft\_server.jar files. If you have already modded them
> they will NOT work with the patches in these scripts.**

**The "test\_game.bat" file uses the "Start.class" file to start the game. This will make sure the game will not
> use your "%APPDATA%\.minecraft" folder, but instead use the "jars" folder for all saves. So any bugs in the modified
> game will not corrupt your normal worlds.**

**If you have any problems using this toolpack, put the "logs\**.log" files that the scripts generated into a
> zip-file and send it to us (post it in the minecraft forum):
> http://www.minecraftforum.net/viewtopic.php?f=25&t=58464

**This version of the mod creator package uses a deobfuscator to change all field and method names in the sources.
> Look in the "conf\minecraft.rgs" and "conf\minecraft\_server.rgs" files for a complete mapping of the names.**

**There are currently no known bugs in the recompiled game or server, except those that were already in the original
> game :) The known bugs, like missing sound effects or the backspace bug in the text entry gui, are fixed with this
> release.**


## Credits: ##

### Searge ###
  * Creator of MCP
  * Fixes all compile errors in the decompiled sourcecode
  * Created the MCP Mod Launcher system and API
### ProfMobius ###
  * Creator of the renaming codes and re-obfuscation procedures
  * Helped to port scripts on Linux
  * Developer and maintainer of the MCP chan bot
  * Is now bald after working too much with java constant pool and re-obfuscation
### IngisKahn ###
  * Creator of the bytecode compare tool that helps us to update the name mappings quickly for new minecraft versions
  * Contributed to the de-obfuscation spreadsheet
### Generic ###
  * Works on improving IngisKahn's bytecode compare tool
  * Added some important features to retroguard
### fotoply ###
  * Helped to improve the batch files
### Fesh0r ###
  * php/sql code monkey
  * MCP 2.6/2.7 class mappings, patches, and general release work
  * Has Searge's approval to make official MCP releases ;)
### Cadde ###
  * Community manager and Wiki manager
  * Works on the de-obfuscation spreadsheet
  * Mod support (making old mods work with MCP)
  * All round handyman
### Vaprtek ###
  * Works on The de-obfuscation spreadsheet
  * Knows how to make pet creepers
### gronk ###
  * Script support
### n00bish ###
  * Linux script maintenance
### Sage Pourpre ###
  * His thread in the forums inspired me (Searge) to create this toolpack in the first place
### Tei ###
  * Supported the MCP project since the first version was released
### spec10 ###
  * The new linux scripts guy
### Head ###
  * Wiki contributor / Administrator
  * Explains classes and their members on the Wiki
### MissLil ###
  * Various scripting stuff
  * Lots of reverse engineering
  * OpenGL constants annoting
### ScottyDoesKnow ###
  * obfuscathonCharmer, the obfuscathon GUI
### Tahg ###
  * Server class mappings
### Chase ###
  * MCP Launcher Work
  * External jar loading
  * Scrollable mod list

### and of course: ###
  * Everybody who contributed to the great google spreadsheet or who created some mods (I've got them all :).
  * NOTCH for creating a game that is just awesome, I hope he does not feel offended by our decompiling efforts.

```
Please, Notch, support our ambitions to mod your game. I know people who bought it just because some great mods.
```

## History ##

  * 2.8  - Added the MCP mod system SDK and support for OSX
  * 2.7  - Updated to support Minecraft 1.2\_02 and MinecraftServer 1.2\_01
  * 2.6  - Updated to support Minecraft 1.1\_02 and MinecraftServer 1.1\_02
  * 2.5  - Updated to support Minecraft 1.2.6 and MinecraftServer 0.2.8
  * 2.4  - Updated to support Minecraft 1.2.5 and MinecraftServer 0.2.7
  * 2.3  - Updated to support Minecraft 1.2.3\_04 and MinecraftServer 0.2.5\_02. Linux support beta.
  * 2.2a - Bugfix release to improve the re-obfuscation tools
  * 2.2  - The reobfuscation beta test release. Still for Minecraft 1.2.2
  * 2.1  - Updated to support Minecraft 1.2.2
  * 2.0a - Bugfix release
  * 2.0  - Major updates to MCP and support for post-Halloween versions of Minecraft
  * 1.6  - All classes have meaningful names now, the class name mappings and the field name mappings are applied
  * 1.5  - Extend the scripts to also support decompiling, recompiling and testing the minecraft\_server.jar file
  * 1.4  - Using a deobfuscator to rename all fields and methods and jadretro to fix some decompile bugs
  * 1.3  - Added upgrade scripts to decompile and recompile Minecraft.class, MinecraftApplet.class and MinecraftServer.class
  * 1.2  - Redirect output of all tools to a logfile
  * 1.1  - Fixed TNT bug
  * 1.0  - First release
```
TODO: make this list the older versions
```

## Roadmap ##

  * 2.9+ - New awesome features, improvements and updates :)