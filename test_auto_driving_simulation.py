#!/usr/bin/env python3
"""
Unit tests for the Auto Driving Car Simulation.
"""

import unittest
from unittest.mock import patch, MagicMock, call
import io
import sys
from typing import Dict, List, Tuple, Any

from auto_driving_simulation import (DirectionEnum, Direction, CommandEnum,
                                     Command, Position, Car, Field, Simulation,
                                     UserInterfaceBase, CommandLineInterface)


class TestDirectionEnum(unittest.TestCase):
  """Test cases for DirectionEnum class."""

  def test_direction_values(self) -> None:
    """Test that the direction enum has the correct values."""
    self.assertEqual(DirectionEnum.NORTH.value, 'N')
    self.assertEqual(DirectionEnum.SOUTH.value, 'S')
    self.assertEqual(DirectionEnum.EAST.value, 'E')
    self.assertEqual(DirectionEnum.WEST.value, 'W')


class TestDirection(unittest.TestCase):
  """Test cases for Direction class."""

  def test_left_rotation(self) -> None:
    """Test left rotation mapping."""
    self.assertEqual(Direction.LEFT_ROTATION[DirectionEnum.NORTH],
                     DirectionEnum.WEST)
    self.assertEqual(Direction.LEFT_ROTATION[DirectionEnum.WEST],
                     DirectionEnum.SOUTH)
    self.assertEqual(Direction.LEFT_ROTATION[DirectionEnum.SOUTH],
                     DirectionEnum.EAST)
    self.assertEqual(Direction.LEFT_ROTATION[DirectionEnum.EAST],
                     DirectionEnum.NORTH)

  def test_right_rotation(self) -> None:
    """Test right rotation mapping."""
    self.assertEqual(Direction.RIGHT_ROTATION[DirectionEnum.NORTH],
                     DirectionEnum.EAST)
    self.assertEqual(Direction.RIGHT_ROTATION[DirectionEnum.EAST],
                     DirectionEnum.SOUTH)
    self.assertEqual(Direction.RIGHT_ROTATION[DirectionEnum.SOUTH],
                     DirectionEnum.WEST)
    self.assertEqual(Direction.RIGHT_ROTATION[DirectionEnum.WEST],
                     DirectionEnum.NORTH)

  def test_movement(self) -> None:
    """Test movement mapping."""
    self.assertEqual(Direction.MOVEMENT[DirectionEnum.NORTH], (0, 1))
    self.assertEqual(Direction.MOVEMENT[DirectionEnum.SOUTH], (0, -1))
    self.assertEqual(Direction.MOVEMENT[DirectionEnum.EAST], (1, 0))
    self.assertEqual(Direction.MOVEMENT[DirectionEnum.WEST], (-1, 0))

  def test_is_valid(self) -> None:
    """Test direction validation."""
    self.assertTrue(Direction.is_valid('N'))
    self.assertTrue(Direction.is_valid('S'))
    self.assertTrue(Direction.is_valid('E'))
    self.assertTrue(Direction.is_valid('W'))
    self.assertFalse(Direction.is_valid('X'))
    self.assertFalse(Direction.is_valid(''))


class TestCommandEnum(unittest.TestCase):
  """Test cases for CommandEnum class."""

  def test_command_values(self) -> None:
    """Test that the command enum has the correct values."""
    self.assertEqual(CommandEnum.LEFT.value, 'L')
    self.assertEqual(CommandEnum.RIGHT.value, 'R')
    self.assertEqual(CommandEnum.FORWARD.value, 'F')


class TestCommand(unittest.TestCase):
  """Test cases for Command class."""

  def test_is_valid(self) -> None:
    """Test command validation."""
    self.assertTrue(Command.is_valid('L'))
    self.assertTrue(Command.is_valid('R'))
    self.assertTrue(Command.is_valid('F'))
    self.assertFalse(Command.is_valid('X'))
    self.assertFalse(Command.is_valid(''))


class TestPosition(unittest.TestCase):
  """Test cases for Position class."""

  def test_init(self) -> None:
    """Test position initialization."""
    pos = Position(10, 20)
    self.assertEqual(pos.x, 10)
    self.assertEqual(pos.y, 20)

  def test_equality(self) -> None:
    """Test position equality comparison."""
    pos1 = Position(10, 20)
    pos2 = Position(10, 20)
    pos3 = Position(20, 10)
    self.assertEqual(pos1, pos2)
    self.assertNotEqual(pos1, pos3)
    self.assertNotEqual(pos1, "not a position")

  def test_hash(self) -> None:
    """Test position hashing for use in dictionaries."""
    pos1 = Position(10, 20)
    pos2 = Position(10, 20)
    pos3 = Position(20, 10)

    # Test that equal positions have equal hashes
    self.assertEqual(hash(pos1), hash(pos2))

    # Test positions as dictionary keys
    pos_dict = {pos1: "position1", pos3: "position3"}
    self.assertEqual(pos_dict[pos2],
                     "position1")  # pos2 should find pos1's value

  def test_get_new_position(self) -> None:
    """Test getting a new position with delta applied."""
    pos = Position(10, 20)
    new_pos = pos.get_new_position(5, -10)
    self.assertEqual(new_pos.x, 15)
    self.assertEqual(new_pos.y, 10)

    # Original position should not change
    self.assertEqual(pos.x, 10)
    self.assertEqual(pos.y, 20)

  def test_string_representation(self) -> None:
    """Test string representation of position."""
    pos = Position(10, 20)
    self.assertEqual(str(pos), "(10,20)")
    self.assertEqual(repr(pos), "(10,20)")


class TestCar(unittest.TestCase):
  """Test cases for Car class."""

  def setUp(self) -> None:
    """Set up test cases."""
    self.pos = Position(5, 5)
    self.car = Car("TestCar", self.pos, DirectionEnum.NORTH)

  def test_init(self) -> None:
    """Test car initialization."""
    self.assertEqual(self.car.name, "TestCar")
    self.assertEqual(self.car.position, self.pos)
    self.assertEqual(self.car.direction, DirectionEnum.NORTH)
    self.assertEqual(self.car.commands, "")
    self.assertFalse(self.car.collided)
    self.assertIsNone(self.car.collision_step)
    self.assertIsNone(self.car.collision_with)

  def test_add_commands(self) -> None:
    """Test adding commands to a car."""
    self.car.add_commands("LRFRL")
    self.assertEqual(self.car.commands, "LRFRL")

  def test_rotate_left(self) -> None:
    """Test rotating car to the left."""
    self.car.direction = DirectionEnum.NORTH
    self.car.rotate_left()
    self.assertEqual(self.car.direction, DirectionEnum.WEST)
    self.car.rotate_left()
    self.assertEqual(self.car.direction, DirectionEnum.SOUTH)
    self.car.rotate_left()
    self.assertEqual(self.car.direction, DirectionEnum.EAST)
    self.car.rotate_left()
    self.assertEqual(self.car.direction, DirectionEnum.NORTH)

  def test_rotate_right(self) -> None:
    """Test rotating car to the right."""
    self.car.direction = DirectionEnum.NORTH
    self.car.rotate_right()
    self.assertEqual(self.car.direction, DirectionEnum.EAST)
    self.car.rotate_right()
    self.assertEqual(self.car.direction, DirectionEnum.SOUTH)
    self.car.rotate_right()
    self.assertEqual(self.car.direction, DirectionEnum.WEST)
    self.car.rotate_right()
    self.assertEqual(self.car.direction, DirectionEnum.NORTH)

  def test_move_forward_within_boundaries(self) -> None:
    """Test moving car forward within field boundaries."""
    field = Field(10, 10)
    self.car.position = Position(5, 5)

    # Test moving north
    self.car.direction = DirectionEnum.NORTH
    result = self.car.move_forward(field)
    self.assertTrue(result)
    self.assertEqual(self.car.position.x, 5)
    self.assertEqual(self.car.position.y, 6)

    # Test moving east
    self.car.direction = DirectionEnum.EAST
    result = self.car.move_forward(field)
    self.assertTrue(result)
    self.assertEqual(self.car.position.x, 6)
    self.assertEqual(self.car.position.y, 6)

    # Test moving south
    self.car.direction = DirectionEnum.SOUTH
    result = self.car.move_forward(field)
    self.assertTrue(result)
    self.assertEqual(self.car.position.x, 6)
    self.assertEqual(self.car.position.y, 5)

    # Test moving west
    self.car.direction = DirectionEnum.WEST
    result = self.car.move_forward(field)
    self.assertTrue(result)
    self.assertEqual(self.car.position.x, 5)
    self.assertEqual(self.car.position.y, 5)

  def test_move_forward_out_of_boundaries(self) -> None:
    """Test moving car forward outside field boundaries."""
    field = Field(10, 10)

    # Test moving north out of bounds
    self.car.position = Position(5, 9)
    self.car.direction = DirectionEnum.NORTH
    result = self.car.move_forward(field)
    self.assertFalse(result)
    self.assertEqual(self.car.position.x, 5)
    self.assertEqual(self.car.position.y, 9)

    # Test moving east out of bounds
    self.car.position = Position(9, 5)
    self.car.direction = DirectionEnum.EAST
    result = self.car.move_forward(field)
    self.assertFalse(result)
    self.assertEqual(self.car.position.x, 9)
    self.assertEqual(self.car.position.y, 5)

    # Test moving south out of bounds
    self.car.position = Position(5, 0)
    self.car.direction = DirectionEnum.SOUTH
    result = self.car.move_forward(field)
    self.assertFalse(result)
    self.assertEqual(self.car.position.x, 5)
    self.assertEqual(self.car.position.y, 0)

    # Test moving west out of bounds
    self.car.position = Position(0, 5)
    self.car.direction = DirectionEnum.WEST
    result = self.car.move_forward(field)
    self.assertFalse(result)
    self.assertEqual(self.car.position.x, 0)
    self.assertEqual(self.car.position.y, 5)

  def test_execute_command(self) -> None:
    """Test executing commands."""
    field = Field(10, 10)
    self.car.position = Position(5, 5)
    self.car.direction = DirectionEnum.NORTH

    # Test left command
    result = self.car.execute_command(CommandEnum.LEFT, field)
    self.assertTrue(result)
    self.assertEqual(self.car.direction, DirectionEnum.WEST)

    # Test right command
    result = self.car.execute_command(CommandEnum.RIGHT, field)
    self.assertTrue(result)
    self.assertEqual(self.car.direction, DirectionEnum.NORTH)

    # Test forward command
    result = self.car.execute_command(CommandEnum.FORWARD, field)
    self.assertTrue(result)
    self.assertEqual(self.car.position.y, 6)

  def test_get_position(self) -> None:
    """Test getting car position."""
    pos = Position(3, 4)
    self.car.position = pos
    self.assertEqual(self.car.get_position(), pos)

  def test_mark_collision(self) -> None:
    """Test marking a car collision."""
    self.car.mark_collision(5, "OtherCar")
    self.assertTrue(self.car.collided)
    self.assertEqual(self.car.collision_step, 5)
    self.assertEqual(self.car.collision_with, "OtherCar")

  def test_string_representation(self) -> None:
    """Test string representation of car."""
    self.car.position = Position(3, 4)
    self.car.direction = DirectionEnum.EAST

    # Normal car
    self.assertEqual(str(self.car), "- TestCar, (3,4) E")

    # Collided car
    self.car.mark_collision(3, "Car2")
    self.assertEqual(str(self.car),
                     "- TestCar, collides with Car2 at (3,4) at step 3")


class TestField(unittest.TestCase):
  """Test cases for Field class."""

  def test_init(self) -> None:
    """Test field initialization."""
    field = Field(10, 20)
    self.assertEqual(field.width, 10)
    self.assertEqual(field.height, 20)

  def test_is_within_boundaries(self) -> None:
    """Test position boundary checking."""
    field = Field(10, 10)

    # Test positions within boundaries
    self.assertTrue(field.is_within_boundaries(Position(0, 0)))
    self.assertTrue(field.is_within_boundaries(Position(9, 9)))
    self.assertTrue(field.is_within_boundaries(Position(5, 5)))

    # Test positions outside boundaries
    self.assertFalse(field.is_within_boundaries(Position(-1, 5)))
    self.assertFalse(field.is_within_boundaries(Position(5, -1)))
    self.assertFalse(field.is_within_boundaries(Position(10, 5)))
    self.assertFalse(field.is_within_boundaries(Position(5, 10)))
    self.assertFalse(field.is_within_boundaries(Position(-1, -1)))
    self.assertFalse(field.is_within_boundaries(Position(10, 10)))


class TestSimulation(unittest.TestCase):
  """Test cases for Simulation class."""

  def setUp(self) -> None:
    """Set up test cases."""
    self.field = Field(10, 10)
    self.simulation = Simulation(self.field)

  def test_init(self) -> None:
    """Test simulation initialization."""
    self.assertEqual(self.simulation.field, self.field)
    self.assertEqual(self.simulation.cars, {})

  def test_add_car(self) -> None:
    """Test adding a car to the simulation."""
    car = Car("TestCar", Position(5, 5), DirectionEnum.NORTH)
    self.simulation.add_car(car)
    self.assertEqual(len(self.simulation.cars), 1)
    self.assertEqual(self.simulation.cars["TestCar"], car)

    # Add another car
    car2 = Car("TestCar2", Position(6, 6), DirectionEnum.SOUTH)
    self.simulation.add_car(car2)
    self.assertEqual(len(self.simulation.cars), 2)
    self.assertEqual(self.simulation.cars["TestCar2"], car2)

  def test_run_simulation_empty(self) -> None:
    """Test running simulation with no cars."""
    # This should not raise any exceptions
    self.simulation.run_simulation()
    self.assertEqual(self.simulation.cars, {})

  def test_run_simulation_single_car(self) -> None:
    """Test running simulation with a single car."""
    car = Car("TestCar", Position(5, 5), DirectionEnum.NORTH)
    car.add_commands("FFLFF")
    self.simulation.add_car(car)

    self.simulation.run_simulation()

    # After FFLFF commands, car should be at (3,7) facing west
    self.assertEqual(car.position.x, 3)
    self.assertEqual(car.position.y, 7)
    self.assertEqual(car.direction, DirectionEnum.WEST)
    self.assertFalse(car.collided)

  def test_run_simulation_collision_detection(self) -> None:
    """Test collision detection during simulation."""
    car1 = Car("Car1", Position(5, 5), DirectionEnum.NORTH)
    car1.add_commands("FF")  # Will end at (5,7)

    car2 = Car("Car2", Position(5, 9), DirectionEnum.SOUTH)
    car2.add_commands("FF")  # Will end at (5,7) - collision!

    self.simulation.add_car(car1)
    self.simulation.add_car(car2)

    self.simulation.run_simulation()

    # Both cars should be marked as collided
    self.assertTrue(car1.collided)
    self.assertTrue(car2.collided)

    # Check collision details
    self.assertEqual(car1.collision_step, 2)
    self.assertEqual(car1.collision_with, "Car2")
    self.assertEqual(car2.collision_step, 2)
    self.assertEqual(car2.collision_with, "Car1")

    # Both cars should be at the collision point
    self.assertEqual(car1.position, Position(5, 7))
    self.assertEqual(car2.position, Position(5, 7))


class TestCommandLineInterface(unittest.TestCase):
  """Test cases for CommandLineInterface class."""

  def setUp(self) -> None:
    """Set up test cases."""
    self.cli = CommandLineInterface()
    self.field = Field(10, 10)

  @patch('builtins.input', side_effect=["invalid", "5 -1", "5", "10 5"])
  def test_get_field_dimensions(self, mock_input: MagicMock) -> None:
    """Test getting field dimensions with valid and invalid inputs."""
    width, height = self.cli.get_field_dimensions()
    self.assertEqual(width, 10)
    self.assertEqual(height, 5)
    self.assertEqual(mock_input.call_count, 4)

  @patch('builtins.input', side_effect=["invalid", "1"])
  def test_get_option(self, mock_input: MagicMock) -> None:
    """Test getting user option with valid and invalid inputs."""
    option = self.cli.get_option()
    self.assertEqual(option, "1")
    self.assertEqual(mock_input.call_count, 2)

  @patch('builtins.input', return_value="TestCar")
  def test_get_car_name(self, mock_input: MagicMock) -> None:
    """Test getting car name."""
    name = self.cli.get_car_name()
    self.assertEqual(name, "TestCar")

  @patch('builtins.input',
         side_effect=["invalid", "5 5", "5 5 X", "11 5 N", "5 5 N"])
  def test_get_car_position(self, mock_input: MagicMock) -> None:
    """Test getting car position with valid and invalid inputs."""
    position, direction = self.cli.get_car_position(self.field)
    self.assertEqual(position, Position(5, 5))
    self.assertEqual(direction, DirectionEnum.NORTH)
    self.assertEqual(mock_input.call_count, 5)

  @patch('builtins.input', side_effect=["LRXF", "LRF"])
  def test_get_car_commands(self, mock_input: MagicMock) -> None:
    """Test getting car commands with valid and invalid inputs."""
    commands = self.cli.get_car_commands()
    self.assertEqual(commands, "LRF")
    self.assertEqual(mock_input.call_count, 2)


if __name__ == '__main__':
  unittest.main()
