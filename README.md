# cursaver
A collection of terminal screensavers written in Python using the curses library.

## Keyboard commands
- q: Quit
- n: Next screensaver
- m: Change mode specific to current screensaver
- up arrow: Increase frame duration
- down arrow: Decrease frame duration

## Included screensaver modes

### Langton's Ant:
Simple rules lead to complex emergent behavior. The ant has four possible directions; up, down, left and right. If the ant is on a white square (no character) it changes direction to the right and advances. If it is on a black square (marked with '#') it changes direction to the left and advances. As the ant advances, the square left behind changes color.

### John Conway's Game of Life
This cellular automaton simulates the evolution of a grid of cells.
#### Rules:
1. A living cell with two or three neighbors survives.
2. A dead cell with three live neighbors becomes a living cell.
3. All other cells either die or stay dead.

If a endless loop of states is detected, cells will randomly repopulate and the "game" will start over.

### Sorting algorithms
A collection of sorting algorithms that will sort an array of numbers from lowest to highest.
#### Algorithms:
- Selection Sort
- Bubble Sort
- Insert Sort
- Quicksort
