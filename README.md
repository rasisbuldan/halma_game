# Halma Game
Clone this repository
```
git clone https://github.com/rasisbuldan/halma_game
```

To run simply just execute in terminal/cmd:
```
python halma.py
```

Prerequisite: pygame library
Tested on pygame 1.9.6 (Python 3.7.6)
```
pip install pygame
```

Font: Coolvetica (https://www.dafont.com/coolvetica.font)

Inserting custom AI, go to `halma_game/halma_player_XX_A/B.py` with API in function `main`

## Feature
- Game configuration screen with board piece animation
- 8x8 and 10x10 board size (8x8 currently not supported by game model)
- Beautiful Light Mode and Dark Mode 
- AI vs AI or human team picker with customizable color
- Informative team name, move history, and move timer

## Latest Changes
- Added human player support
- Added 4-Player support (Team 2 vs 2)
- Multiple rounds

## To be developed
- Online match
- Debug/Strategy mode built for AI development
- Multiprocessing/Multithreading GUI element and AI computation to be parallel (continuous timer)
- PyPI package

## Screenshot
Dark Mode Starting Screen
![Starting Light Mode](assets/screenshot/starting_dark.png?raw=True)

Light Mode Playing Screen
![Playing Dark Mode](assets/screenshot/playing.png?raw=True)
