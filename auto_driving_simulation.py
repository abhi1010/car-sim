#!/usr/bin/env python3
"""
Auto Driving Car Simulation - A command-line program for simulating autonomous cars
on a rectangular field with collision detection.
"""

import logging
from enum import Enum, auto
from typing import Dict, List, Tuple, Optional, Set, Any, Union
from abc import ABC, abstractmethod

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DirectionEnum(Enum):
  """Represents the four cardinal directions."""
  NORTH = 'N'
  SOUTH = 'S'
  EAST = 'E'
  WEST = 'W'


class Direction:
  """Helper class for direction operations."""
  # Maps for direction rotations
  LEFT_ROTATION: Dict[DirectionEnum, DirectionEnum] = {
      DirectionEnum.NORTH: DirectionEnum.WEST,
      DirectionEnum.WEST: DirectionEnum.SOUTH,
      DirectionEnum.SOUTH: DirectionEnum.EAST,
      DirectionEnum.EAST: DirectionEnum.NORTH
  }

  RIGHT_ROTATION: Dict[DirectionEnum, DirectionEnum] = {
      DirectionEnum.NORTH: DirectionEnum.EAST,
      DirectionEnum.EAST: DirectionEnum.SOUTH,
      DirectionEnum.SOUTH: DirectionEnum.WEST,
      DirectionEnum.WEST: DirectionEnum.NORTH
  }

  # Maps for direction movements
  MOVEMENT: Dict[DirectionEnum, Tuple[int, int]] = {
      DirectionEnum.NORTH: (0, 1),
      DirectionEnum.SOUTH: (0, -1),
      DirectionEnum.EAST: (1, 0),
      DirectionEnum.WEST: (-1, 0)
  }

  @staticmethod
  def is_valid(direction: str) -> bool:
    """Check if a direction is valid."""
    try:
      DirectionEnum(direction)
      return True
    except ValueError:
      return False


class CommandEnum(Enum):
  """Represents the commands that can be issued to cars."""
  LEFT = 'L'
  RIGHT = 'R'
  FORWARD = 'F'


class Command:
  """Helper class for command operations."""

  @staticmethod
  def is_valid(command: str) -> bool:
    """Check if a command is valid."""
    try:
      CommandEnum(command)
      return True
    except ValueError:
      return False


class Position:
  """Represents a position on the field with x and y coordinates."""

  def __init__(self, x: int, y: int):
    self.x: int = x
    self.y: int = y

  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, Position):
      return False
    return self.x == other.x and self.y == other.y

  def __hash__(self) -> int:
    return hash((self.x, self.y))

  def get_new_position(self, delta_x: int, delta_y: int) -> 'Position':
    """Return a new position with the given delta applied."""
    return Position(self.x + delta_x, self.y + delta_y)

  def __str__(self) -> str:
    return f"({self.x},{self.y})"

  def __repr__(self) -> str:
    return self.__str__()


class Car:
  """Represents a car in the simulation."""

  def __init__(self, name: str, position: Position, direction: DirectionEnum):
    """Initialize a car with a name, position, and direction."""
    self.name: str = name
    self.position: Position = position
    self.direction: DirectionEnum = direction
    self.commands: str = ""
    self.collided: bool = False
    self.collision_step: Optional[int] = None
    self.collision_with: Optional[str] = None

  def add_commands(self, commands: str) -> None:
    """Add a sequence of commands to the car."""
    self.commands = commands

  def rotate_left(self) -> None:
    """Rotate the car 90 degrees to the left."""
    self.direction = Direction.LEFT_ROTATION[self.direction]

  def rotate_right(self) -> None:
    """Rotate the car 90 degrees to the right."""
    self.direction = Direction.RIGHT_ROTATION[self.direction]

  def move_forward(self, field: 'Field') -> bool:
    """Move the car forward by 1 grid point if within field boundaries."""
    delta_x, delta_y = Direction.MOVEMENT[self.direction]
    new_position = self.position.get_new_position(delta_x, delta_y)

    # Check if the new position is within the field boundaries
    if field.is_within_boundaries(new_position):
      self.position = new_position
      return True
    return False

  def execute_command(self, command: CommandEnum, field: 'Field') -> bool:
    """Execute a single command."""
    if command == CommandEnum.LEFT:
      self.rotate_left()
      return True
    elif command == CommandEnum.RIGHT:
      self.rotate_right()
      return True
    elif command == CommandEnum.FORWARD:
      return self.move_forward(field)
    return False

  def get_position(self) -> Position:
    """Return the current position of the car."""
    return self.position

  def mark_collision(self, step: int, other_car_name: str) -> None:
    """Mark the car as having collided with another car."""
    self.collided = True
    self.collision_step = step
    self.collision_with = other_car_name

  def __str__(self) -> str:
    """Return a string representation of the car."""
    if self.collided:
      return f"- {self.name}, collides with {self.collision_with} at {self.position} at step {self.collision_step}"
    return f"- {self.name}, {self.position} {self.direction.value}"

  def __repr__(self) -> str:
    return self.__str__()


class Field:
  """Represents the rectangular field where cars operate."""

  def __init__(self, width: int, height: int):
    """Initialize a field with given width and height."""
    self.width: int = width
    self.height: int = height

  def is_within_boundaries(self, position: Position) -> bool:
    """Check if a position is within the field boundaries."""
    return 0 <= position.x < self.width and 0 <= position.y < self.height


class Simulation:
  """Manages the simulation of cars on a field."""

  def __init__(self, field: Field):
    """Initialize a simulation with a field."""
    self.field: Field = field
    self.cars: Dict[str, Car] = {}

  def add_car(self, car: Car) -> None:
    """Add a car to the simulation."""
    self.cars[car.name] = car

  def run_simulation(self) -> None:
    """Run the simulation for all cars."""
    max_commands = max(len(car.commands)
                       for car in self.cars.values()) if self.cars else 0

    # Process commands step by step for each car
    for step in range(max_commands):
      # Store positions of cars after this step to detect collisions
      positions: Dict[Position, str] = {}

      for car_name, car in self.cars.items():
        # Skip if car has already collided or has no more commands
        if car.collided or step >= len(car.commands):
          continue

        # Execute the current command
        command = CommandEnum(car.commands[step])
        car.execute_command(command, self.field)

        # Check for collisions
        position = car.get_position()
        if position in positions:
          # Collision detected
          other_car = self.cars[positions[position]]
          car.mark_collision(step + 1, other_car.name)
          other_car.mark_collision(step + 1, car.name)
        else:
          positions[position] = car_name


class UserInterfaceBase(ABC):
  """Base abstract class for user interfaces."""

  @abstractmethod
  def display_welcome(self) -> None:
    """Display the welcome message."""
    pass

  @abstractmethod
  def get_field_dimensions(self) -> Tuple[int, int]:
    """Get field dimensions from user input."""
    pass

  @abstractmethod
  def display_options(self) -> None:
    """Display the main options."""
    pass

  @abstractmethod
  def get_option(self) -> str:
    """Get user option from input."""
    pass

  @abstractmethod
  def get_car_name(self) -> str:
    """Get car name from user input."""
    pass

  @abstractmethod
  def get_car_position(self, field: Field) -> Tuple[Position, DirectionEnum]:
    """Get car position and direction from user input."""
    pass

  @abstractmethod
  def get_car_commands(self) -> str:
    """Get car commands from user input."""
    pass

  @abstractmethod
  def display_cars(self, cars: Dict[str, Car]) -> None:
    """Display the list of cars."""
    pass

  @abstractmethod
  def display_simulation_results(self, cars: Dict[str, Car]) -> None:
    """Display the results after simulation."""
    pass

  @abstractmethod
  def display_final_options(self) -> None:
    """Display options after simulation."""
    pass

  @abstractmethod
  def get_final_option(self) -> str:
    """Get user final option from input."""
    pass

  @abstractmethod
  def display_exit_message(self) -> None:
    """Display exit message."""
    pass


class CommandLineInterface(UserInterfaceBase):
  """Handles user interaction through the command line."""

  def display_welcome(self) -> None:
    """Display the welcome message."""
    logger.info("Welcome to Auto Driving Car Simulation!")
    logger.info(
        "\nPlease enter the width and height of the simulation field in x y format:"
    )

  def get_field_dimensions(self) -> Tuple[int, int]:
    """Get field dimensions from user input."""
    while True:
      try:
        dimensions = input().strip().split()
        if len(dimensions) != 2:
          logger.info("Please enter two numbers separated by a space.")
          continue

        width = int(dimensions[0])
        height = int(dimensions[1])

        if width <= 0 or height <= 0:
          logger.warning("Width and height must be positive integers.")
          continue

        return width, height
      except ValueError:
        logger.warning("Width and height must be integers.")

  def display_options(self) -> None:
    """Display the main options."""
    logger.info("\nPlease choose from the following options:")
    logger.info("[1] Add a car to field")
    logger.info("[2] Run simulation")

  def get_option(self) -> str:
    """Get user option from input."""
    while True:
      option = input().strip()
      if option in ['1', '2']:
        return option
      logger.warning("Invalid option. Please enter 1 or 2.")

  def get_car_name(self) -> str:
    """Get car name from user input."""
    logger.info("Please enter the name of the car:")
    return input().strip()

  def get_car_position(self, field: Field) -> Tuple[Position, DirectionEnum]:
    """Get car position and direction from user input."""
    logger.info(
        "Please enter initial position of car in x y Direction format:")
    while True:
      try:
        position_input = input().strip().split()
        if len(position_input) != 3:
          logger.info("Please enter x, y, and direction separated by spaces.")
          continue

        x = int(position_input[0])
        y = int(position_input[1])
        direction_str = position_input[2].upper()

        if not Direction.is_valid(direction_str):
          logger.warning("Direction must be N, S, E, or W.")
          continue

        position = Position(x, y)
        direction = DirectionEnum(direction_str)

        if not field.is_within_boundaries(position):
          logger.warning(
              f"Position must be within field boundaries (0,0) to ({field.width-1},{field.height-1})."
          )
          continue

        return position, direction
      except ValueError:
        logger.info("X and Y must be integers.")

  def get_car_commands(self) -> str:
    """Get car commands from user input."""
    logger.info("Please enter the commands for car:")
    while True:
      commands = input().strip().upper()
      if all(Command.is_valid(cmd) for cmd in commands):
        return commands
      logger.info("Commands must be L, R, or F only.")

  def display_cars(self, cars: Dict[str, Car]) -> None:
    """Display the list of cars."""
    logger.info("\nYour current list of cars are:")
    for car_name, car in cars.items():
      logger.info(
          f"- {car.name}, {car.position} {car.direction.value}, {car.commands}"
      )

  def display_simulation_results(self, cars: Dict[str, Car]) -> None:
    """Display the results after simulation."""
    logger.info("\nAfter simulation, the result is:")
    for car in cars.values():
      logger.info(str(car))

  def display_final_options(self) -> None:
    """Display options after simulation."""
    logger.info("\nPlease choose from the following options:")
    logger.info("[1] Start over")
    logger.info("[2] Exit")

  def get_final_option(self) -> str:
    """Get user final option from input."""
    while True:
      option = input().strip()
      if option in ['1', '2']:
        return option
      logger.info("Invalid option. Please enter 1 or 2.")

  def display_exit_message(self) -> None:
    """Display exit message."""
    logger.info("\nThank you for running the simulation. Goodbye!")


def main() -> None:
  """Main function to run the simulation program."""
  # Create the user interface
  ui: UserInterfaceBase = CommandLineInterface()

  while True:
    # Welcome and initialize field
    ui.display_welcome()
    width, height = ui.get_field_dimensions()
    field = Field(width, height)
    logger.info(f"You have created a field of {width} x {height}")

    # Initialize simulation
    simulation = Simulation(field)

    # Main interaction loop
    while True:
      ui.display_options()
      option = ui.get_option()

      if option == '1':  # Add a car
        car_name = ui.get_car_name()

        # Check if car name already exists
        if car_name in simulation.cars:
          logger.info(
              f"Car {car_name} already exists. Please choose a different name."
          )
          continue

        position, direction = ui.get_car_position(field)
        car = Car(car_name, position, direction)

        commands = ui.get_car_commands()
        car.add_commands(commands)

        simulation.add_car(car)
        ui.display_cars(simulation.cars)

      elif option == '2':  # Run simulation
        if not simulation.cars:
          logger.info(
              "No cars have been added to the simulation. Please add at least one car."
          )
          continue

        ui.display_cars(simulation.cars)
        simulation.run_simulation()
        ui.display_simulation_results(simulation.cars)
        break

    # After simulation, ask if user wants to start over or exit
    ui.display_final_options()
    final_option = ui.get_final_option()

    if final_option == '2':  # Exit
      ui.display_exit_message()
      break


if __name__ == "__main__":
  main()
