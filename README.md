# DemandPagingSimulator
This is a Demand Paging Simulator made on python using tkinter for the Operating Systems course at Universidad del Norte.

## Project Description
Make a Demand Paging Simulator with animations

### Specifications
- Inputs are as followed: 
  - Size of page frame
  - Size of the Operative System
  - Size of the process
  - Set of instructions (See [Entrada.csv](./Entrada.csv) for format)
  - List of free page frames in memory
- The program should:
  - Let the user increase and decrease the speed of the instructions and animations
  - Show the process divided in pages in virtual memory
  - Show memory divided in page frames with the ones occupied by the operative system and the free page frames, both given as input
  - Show the behavior of the Page table including the dirty bit and the valid-invalid bit
  - Show the corresponding data for each page frame (Physical address, Page assigned, Page Frame number)
  - Show Swap In and Swap Out process when needed
  - Show total number of Page foults and Swap ins/out
  - Create a file where every step of the process is written
 - The page replacing algorithm is free of choice (We will use LRU)

## Installation
If the python version you are running doesn't include tkinter, then `pip install tkinter`
## Execution
1. Run `anim.py`
2. Remember to create an instruction input file like [Entrada.csv](./Entrada.csv), the program will ask for it
