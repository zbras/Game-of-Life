# Game of Life

######Concept program implementing John Conway's Game of Life, a zero-player game which models population evolution.

Given an intial board state - determined at random - the program will simulate population growth and decay according to the rules prescribed by the game. This program deviates from the rules of the original game in three customizable ways:
> - If a cell is generated offscreen, it will be deleted so as not to generate more cells and consume memory.
> - Every iteration a customizable number of randomly spawning cells is created and destroyed, as to affect the outcomes of the current living and neighboring dead cells. These cells are generated to increase the lifetime of the cells visible in the simulation.
> - If, at any point, there are fewer cells alive in the simulation than the number of randomly spawning cells - and the `REGEN_BOARD_WHEN_EMPTY` flag is set to *True* - the simulation will regenerate a random board state and continue running.

The game can be configured for specific color ranges, a minimum number of cells along the lower resolution, cell border size, time between sequences, whether or not to create a fresh population when the total population reaches a minimum, and a random cell regeneration percentage of the total population of dead and alive cells.

When the program is executed, the mouse will be hidden and a new fullscreen borderless window will be created. After the initial board generation, the program will continue sequencing until the script is terminated (Alt-F4 is your friend). Please note that the program does not support multiple-monitor setups and will default to the primary monitor's resolution.