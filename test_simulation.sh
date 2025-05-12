#!/bin/bash

# Colors for better output readability
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Auto Driving Car Simulation Test Script${NC}"
echo -e "${BLUE}======================================${NC}\n"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
  echo -e "${RED}Error: Python 3 is not installed. Please install Python 3 to run the simulation.${NC}"
  exit 1
fi

# Check if simulation file exists
if [ ! -f "auto_driving_simulation.py" ]; then
  echo -e "${RED}Error: auto_driving_simulation.py not found in current directory.${NC}"
  exit 1
fi

# Function to run a scenario with provided input
run_scenario() {
  local scenario_num=$1
  local description=$2
  local input=$3

  echo -e "${YELLOW}Running Scenario $scenario_num: $description${NC}"
  echo -e "${BLUE}Input:${NC}"
  echo "$input" | sed 's/^/  /'

  echo -e "${BLUE}Output:${NC}"
  echo "$input" | python3 auto_driving_simulation.py | sed 's/^/  /'

  echo -e "${GREEN}Scenario $scenario_num completed${NC}\n"
  echo "Press Enter to continue to the next scenario..."
  read
}

# # Check if unit tests pass
# echo -e "${YELLOW}Running unit tests first...${NC}"
# if [ -f "test_auto_driving_simulation.py" ]; then
#   pytest .
#   test_result=$?
#   if [ $test_result -eq 0 ]; then
#     echo -e "${GREEN}All unit tests passed!${NC}\n"
#   else
#     echo -e "${RED}Unit tests failed. There might be issues with the simulation.${NC}\n"
#     echo "Press Enter to continue with scenarios anyway or Ctrl+C to abort..."
#     read
#   fi
# else
#   echo -e "${YELLOW}Warning: test_auto_driving_simulation.py not found. Skipping unit tests.${NC}\n"
# fi

# Scenario 1: Basic scenario with a single car
scenario1_input="10 10
1
A
1 2 N
FFRFFFFRRL
2
2"

run_scenario 1 "Single car navigation (moves forward, turns, should end at (5,4) S)" "$scenario1_input"

# Scenario 2: Two cars with collision
scenario2_input="10 10
1
A
1 2 N
FFRFFFF
1
B
7 8 W
FFLFFFF
2
2"

run_scenario 2 "Two cars with collision (should collide at (5,4) at step 7)" "$scenario2_input"

# Scenario 3: Car tries to move beyond field boundary
scenario3_input="5 5
1
A
0 0 S
FFF
2
2"

run_scenario 3 "Car trying to move beyond field boundary (should stay at (0,0) S)" "$scenario3_input"

# Scenario 4: Car with no commands
scenario4_input="10 10
1
A
3 3 E

2
2"

run_scenario 4 "Car with no commands (should stay at initial position)" "$scenario4_input"

# Scenario 5: Multiple cars without collision
scenario5_input="10 10
1
A
1 1 N
FRFRFRFR
1
B
8 8 S
FLFLFLFL
2
2"

run_scenario 5 "Multiple cars without collision" "$scenario5_input"

# Scenario 6: Car with only rotation commands
scenario6_input="10 10
1
A
5 5 N
LRLRLRLR
2
2"

run_scenario 6 "Car with only rotation commands (should end at (5,5) N)" "$scenario6_input"

# Scenario 7: Three cars with one collision
scenario7_input="10 10
1
A
1 1 E
FFFFFRFF
1
B
8 1 W
FFFFFLFF
1
C
5 5 S
FFF
2
2"

run_scenario 7 "Three cars with one collision" "$scenario7_input"

# Scenario 8: Larger field
scenario8_input="20 20
1
A
10 10 N
FFFFFFFFFF
2
2"

run_scenario 8 "Car on a larger field" "$scenario8_input"

# Scenario 9: Multiple collisions in sequence
scenario9_input="10 10
1
A
1 5 E
FFFF
1
B
5 5 W
FFFF
1
C
3 5 E
FFFF
2
2"

run_scenario 9 "Multiple sequential collisions" "$scenario9_input"

# Scenario 10: Complex movement pattern
scenario10_input="15 15
1
X
7 7 N
FFRFFLFFLFFRRFLF
2
2"

run_scenario 10 "Complex movement pattern" "$scenario10_input"

echo -e "${GREEN}All scenarios have been completed!${NC}"
echo "This script has demonstrated various capabilities of the simulation including:"
echo "  - Basic car movement and rotation"
echo "  - Collision detection"
echo "  - Boundary enforcement"
echo "  - Multiple car handling"
echo "  - Complex movement patterns"
echo ""
echo -e "${BLUE}Thank you for using the Auto Driving Car Simulation!${NC}"