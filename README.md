# Game of Life

***Concept program implementing John Conway's Game of Life, a zero-player game which models population evolution.***

Given an intial board state - determined at random - the program will simulate population growth and decay according to the rules prescribed by the game. This program deviates from the rules of the original game in three customizable ways:
> - If a cell is generated offscreen, it will be deleted so as not to generate more cells and consume memory.
> - Every iteration a customizable number of randomly spawning cells is created and destroyed, as to affect the outcomes of the current living and neighboring dead cells. These cells are generated to increase the lifetime of the cells visible in the simulation.
> - If, at any point, there are fewer cells alive in the simulation than the number of randomly spawning cells - and the `REGEN_BOARD_WHEN_EMPTY` flag is set to ***True*** - the simulation will regenerate a random board state and continue running.

The game can be configured for specific color and brightness ranges, a minimum number of cells along the lower resolution, cell border size, time between sequences, whether or not to create a fresh population when the total population reaches a minimum, and a random cell regeneration percentage of the total population of dead and alive cells.

At the title screen, left click or press ***Enter*** to begin the simulation. Pressing ***Escape*** at any time will close the program. You may toggle the simulation by pressing the ***Left mouse button***, and open the options menu with ***Tab***. Please note that the program does not support multiple-monitor setups and will default to the primary monitor's resolution.