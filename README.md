
Aerial Library
==============

Python library for the robo4you Aerial Junior Challenge 2025.

Enables simple, intuitive interaction with the Crazyflie 2.1 drone.


Usage
-----

For detailed description, see the documentation of `Drone`.

Basic usage:
```python
from aerial_library import Drone


with Drone() as drone:
    drone.takeoff(1.0)
    
    drone.forward(0.5)
    drone.back(0.5)
    drone.left(0.5)
    drone.right(0.5)
    
    drone.up(0.5)
    drone.down(0.5)
    
    drone.turn_left(90)
    drone.turn_right(90)
    
    drone.land()
```


Installation
------------

> [!NOTE]
> TODO: provide package somewhere
> 
> For now, run `uv build` and install the `.whl` file to your interpreter using `pip`


---

Developer Roadmap
-----------------

* [ ] Provide library as some package
* [ ] Provide documentation
* [ ] Fix `Error no LogEntry to handle id=...`
* [ ] Make all but `Drone` actually package-private
* [ ] Finalise [pyproject.toml](./pyproject.toml)
* [ ] Provide developer docs/info about implementation
