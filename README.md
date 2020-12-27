# ps2tool
Simple GUI to change some options not accessible via the main Planetside 2 application.  Also includes population viewer.

## Features
- Start Recursion tracker and the Launchpad at the same time.
- Choose any .ttf font to use as the in game font.
- Choose between multiple .ini files to use as UserOptions.ini.
- Choose tint colours for infantry reticules, no deploy zones, and orbital strikes.
- Population viewer for Connery, Miller, Cobalt, Emerald, and Soltech.  Uses fisu's population API https://ps2.fisu.pw/api/population/.

## Download
- https://github.com/windalin/ps2tool/releases

## Instructions
1. Download and install Python 3 https://www.python.org/downloads/.
2. Extract `ps2tool.py`, `settings.txt`, and `Geo-Md.ttf` to your Planetside 2 folder.
3. Create a shortcut of `ps2tool.py` and put it somewhere convenient.  You can change its icon to `LaunchPad.ico`.

- **Important: wait for the launchpad to download any updates and let the play button light up before clicking** `Apply changes`**.**
- **TintModeReticuleStyle must be set to 1 under UserOptions.ini/UI in order to use custom reticule colours.**

## Notes
- Geo-Md.ttf is the original font that the game uses.  The tool copies Geo-Md.ttf to UI/Resource/Fonts/Geo-Md.ttf before starting the launchpad, preventing it from downloading Geo-Md.ttf if a different font was previously used.  This prevents login issues if the download servers are down but game servers are up.  See https://twitter.com/AndySites/status/1327365280515801088.
- Newly tracked directives are currently not copied to different .ini files.
- Alternative fonts must be .ttf files.
- If you don't want the command window to appear when starting the tool, change the extension of `ps2tool.py` from `.py` to `.pyw`
