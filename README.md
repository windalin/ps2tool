# ps2tool

![image](https://user-images.githubusercontent.com/45084896/165137417-92845c92-a44d-4a3d-ac45-e6991e88c14f.png)

## Features
- Choose between multiple .ttf fonts to use as the in game font.
- Choose between multiple .ini files to use as UserOptions.ini.
- Choose tint colour for infantry reticules.
- Population viewer for Connery, Miller, Cobalt, Emerald, and Soltech.  Uses Honu's population API, see https://wt.honu.pw/api-doc/index.html.
- Automatically start the launchpad and Recursion stat tracker.

**Important:**
- **Wait for the launchpad to download any updates and let the `>> PLAY <<` button light up before clicking** `Apply changes`**.**  
- **This tool does not validate that the currently selected .ini is valid, please ensure that the selected .ini file is valid before using it.**

## Download
- https://github.com/windalin/ps2tool/releases

## Installation
1. Download and install Python 3 https://www.python.org/downloads/.
2. Extract `Installer.py` and the `ps2tool` folder somewhere convenient.
3. Run `Installer.py`.

To uninstall, just delete the `ps2tool` folder where you installed it.

## Notes
- Geo-Md.ttf is the original font that the game uses.  The tool copies Geo-Md.ttf to UI/Resource/Fonts/Geo-Md.ttf before starting the launchpad, preventing it from redownloading Geo-Md.ttf if a different font was previously used.  This prevents login issues if the download servers are down but game servers are up.  See https://twitter.com/AndySites/status/1327365280515801088.
- Newly tracked directives are currently not copied to different .ini files.
- Alternative fonts must be .ttf files.
