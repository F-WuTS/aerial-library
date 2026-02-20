
Aerial Library
==============

Python library for the robo4you Aerial Junior Challenge.

Enables simple, intuitive interaction with the Crazyflie 2.1 drone.


Usage
-----
For detailed description, see the documentation of `Drone`.

Basic usage:
```py
from aerial_library import Drone, FlowDeck

with Drone("E7E7E7E7E7", FlowDeck) as drone:
    drone.takeoff(1.0)
    drone.move_forward(0.5)
```


Installation
------------
With your venv active, use `pip` to install the package directly from this repository:
```sh
pip install git+https://github.com/F-WuTS/aerial-library.git
```


