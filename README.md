<!-- ![](https://img.shields.io/codefactor/grade/github/Darkempire78/Github1s-Extension?style=for-the-badge) ![](https://img.shields.io/github/repo-size/Darkempire78/Github1s-Extension?style=for-the-badge) --> <a href="https://discord.com/invite/sPvJmY7mcV"><img src="https://img.shields.io/discord/831524351311609907?color=%237289DA&label=DISCORD&style=for-the-badge"></a>

#  Readme 2048

This template repository contains the source code for a Python 2048 automatic bot, together with GitHub Workflows in order to allow ANYONE to play 2048 from a README file. Want to see this in action? Go to my profile page and feel free to try it out by yourself!

<img src="https://github.com/Darkempire78/readme-2048/blob/main/Capture1.PNG" width="500"/>

## Steps to make your own repo

1. Click on `"Use this template"`.

2. Replace the the link (`https://github.com/Darkempire78/Readme-2048`) to the link of your own repository in each files.

3. Rename the folder `.github/_workflows` to `.github/workflows`.

4. Delete this README file and make your own `README.md` based on the `README.template.md`. Do not forget that the both comments `"<-- 2048GameActions -->"` and `"<-- 2048Ranking -->"` cannot be deleted!

## Themes
You can change the theme of the gameboard between dark and light mode editing `config.json`.

## Features

* Play to 2048
* Archive games
* Leaderboard
* Dark mode


## Archives

The current game is always called `Data/Games/current.json`. All games are automatically archived into the `Data/Games/` folder.

## To do
- [ ] Remove impossible actions
- [ ] Do not download Pillow each time 
- [ ] Prevent from runing twice actions at the same time (https://github.com/marketplace/actions/wait-for-check)

## Discord

Join the Discord server !

[![](https://i.imgur.com/UfyvtOL.png)](https://discord.gg/sPvJmY7mcV)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is under [GPLv3](LICENSE).
