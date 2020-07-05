# Racing (game)

This is a project I've done to study `neat-python` package. Also used: `pygame`.

It is a racing game: there is a track and a car, controlled by player (or AI). The task is to drive the car on the track. If car is on the grass than game is over. Player (or AI) can select velocity and angular velocity of car from fixed ranges. There are several radars on the car, which measure distance from the center of the car to the border of the road. NEAT studies by taking the results of the measures from the car and passing `gas` and `turn` intesivity to it. The greater car velocity or the less car angular velocity the greater fitness of the genome of the NEAT.

## Installation

First, run following command to install pygame dependencies:
```
sudo apt build-dep python-pygame -y
```

Second, clone this repo.

Third, go to the folder of repo and install virtual enviroment:
```
pipenv install
```
To play the game run
```
pipenv run python play.py
```
To start ai playing this game run
```
pipenv run python aidriver.py
```
