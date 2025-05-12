# Auto Driving Car Simulation

A command-line program that simulates autonomous cars on a rectangular field with collision detection.

## Functional Features

- Create a simulation field with custom dimensions
- Add multiple cars with unique names, positions, and directions
- Control cars using simple commands (left turn, right turn, forward movement)
- Run simulations with step-by-step processing
- Detect and report collisions between cars
- Prevent cars from moving beyond field boundaries

## Requirements

```bash

virtualenv -p python3 ve
source ve/bin/activate
pip install -r ./requirements.txt

```


## How to Run



```bash
python auto_driving_simulation.py
```


## Running Tests

To run the test suite and verify the program's functionality:

```bash
pytest . # simple pytests
pytest --cov # pytests with coverage

```



## Sample test simulation

There are a lot of scenarios that can be tested by running the `test_simulation.sh` script.

```bash

./test_simulation.sh
```


## Possible Improvements


### Code Structure and Design Improvements

* **Constants File**: Move magic strings and values to a constants file or configuration.

### Error Handling and Logging

* **Logging Strategy**: Implement a more sophisticated logging strategy with different log levels for different parts of the system.
* **User Feedback**: Improve error messages to be more specific and helpful.



### Feature Enhancements

* **Save/Load Functionality**: Add ability to save and load simulation states.
* **Simulation Speed Control**: Allow users to control the speed of the simulation.
* **Batch Processing**: Support batch simulation runs from configuration files.
* **Advanced Collision Handling**: Implement more sophisticated collision rules.
* **Command-line Arguments**: Support command-line arguments for non-interactive use.
