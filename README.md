# ps2tool

![image](https://user-images.githubusercontent.com/45084896/165137417-92845c92-a44d-4a3d-ac45-e6991e88c14f.png)

## Features
- Choose between multiple .ttf fonts to use as the in game font.
- Choose between multiple .ini files to use as UserOptions.ini.
- Choose tint colour for infantry reticules.
- Population viewer for Connery, Miller, Cobalt, Emerald, and SolTech.  Uses Honu's population API, see https://wt.honu.pw/api-doc/index.html.
- Automatically start the launchpad and Recursion stat tracker.
- Automatically click the play button (optional, requires PyGetWindow and PyAutoGUI).

**Important:**
- **Wait for the launchpad to download any updates and let the `>> PLAY <<` button light up before clicking** `Apply changes`**.**  
- **This program does not validate that the currently selected .ini is valid, please ensure that the selected .ini file is valid before using it.**

## Download
- https://github.com/windalin/ps2tool/releases

## Installation
### Executable version:
Extract the `ps2tool` folder somewhere convenient.

### Installer version:

**! This program currently doesn't work when installed under C:\Program Files, pick somewhere else for now.**
1. Download and install Python 3 https://www.python.org/downloads/.
2. Extract `Installer.py` and the `ps2tool` folder somewhere convenient.
3. Run `Installer.py`.

To uninstall, just delete the `ps2tool` folder where you installed it.

## Notes
- Geo-Md.ttf is the original font that the game uses.  The program copies Geo-Md.ttf to UI/Resource/Fonts/Geo-Md.ttf before starting the launchpad, preventing it from redownloading Geo-Md.ttf if a different font was previously used.  This prevents login issues if the download servers are down but game servers are up.  See https://twitter.com/AndySites/status/1327365280515801088.
- Newly tracked directives are currently not copied to different .ini files.
- Alternative fonts must be .ttf files.
- This project is written in Python 3.8 for Windows 10 and may not work on older versions of Python and/or other operating systems.

## Disclaimer
- You (the user) assume full responsibility and liability by using this program and its features, including but not limited to: changing font, changing UserOptions.ini, enabling custom reticule colours, changing custom reticule colour.  I (the author of this project) am not responsible nor liable for any ban(s) to your Daybreak Games/Planetside 2 account(s) as a result.
- Changing the ingame font is currently not bannable (see: [Daybreak Games forum thread](https://forums.daybreakgames.com/ps2/index.php?threads/will-changing-the-font-in-game-get-me-banned.78236/), mirror: [Wayback Machine](https://web.archive.org/web/20220424191522/https://forums.daybreakgames.com/ps2/index.php?threads/will-changing-the-font-in-game-get-me-banned.78236/)), however this may change in the future at the discretion of Daybreak Games.
- Using custom reticule colours is currently not bannable (see: [reddit thread](https://www.reddit.com/r/Planetside/comments/2tq92i/psa_you_can_customize_the_color_of_your_reticules/), mirror: [Wayback Machine](http://web.archive.org/web/20220425173729/https://www.reddit.com/r/Planetside/comments/2tq92i/psa_you_can_customize_the_color_of_your_reticules/)), however this may change in the future at the discretion of Daybreak Games.
