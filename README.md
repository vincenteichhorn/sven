# Installation
```shell
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```
## Maybe manually install torch cpu
```shell
pip3 install torch --index-url https://download.pytorch.org/whl/cpu
```

# Tool
```
usage: learn.py [-h] [--file FILE] [--all | --no-all] [--cache | --no-cache] [--game | --no-game]

options:
  -h, --help           show this help message and exit
  --file FILE          Path to the questions csv file
  --all, --no-all      Learn additional questions, not only the ones from Sven
  --cache, --no-cache  Cache your answers
  --game, --no-game    Game mode
```
## Learn Mode
```shell
python3 -m sven.learn
```

## Game Mode
```shell
python3 -m sven.learn --game
```