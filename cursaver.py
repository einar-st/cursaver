import curses
from ant import ant_init, ant_update
from game_of_life import gol_init, gol_update
from sort import sort_init, sort_update
from funcs import draw_str, cycle
from time import time


def main(stdscr):

    # Setup
    start = time()
    title_start = time()
    curses.curs_set(0)  # hide cursor
    curses.use_default_colors()
    stdscr.nodelay(1)  # non-blocking input
    cycle_savers = False
    cycle_duration = 45  # duration in minutes
    maxy, maxx = stdscr.getmaxyx()

    init = {
        'ant': ant_init,
        'gol': gol_init,
        'sort': sort_init
    }

    update = {
        'ant': ant_update,
        'gol': gol_update,
        'sort': sort_update
    }

    modes = ['ant', 'gol', 'sort']
    mode = 0
    frame_count = 0

    data = init[modes[mode]](maxx, maxy)
    rate = data['rate']
    stdscr.timeout(data['rate'])

    # Main loop
    while True:

        # change mode if time interval has passed
        if cycle_savers and (time() - start >= cycle_duration * 60):
            mode = cycle(mode, len(modes) - 1)
            data = init[modes[mode]](maxx, maxy)
            start, title_start = time(), time()

        # User input
        key = stdscr.getch()
        if key == ord('q'):
            break  # Exit the loop if 'q' is pressed
        elif key == 259:
            data['rate'] += 5
            stdscr.timeout(data['rate'])
            title_start = time()
        elif key == 258:
            data['rate'] -= 5
            data['rate'] = max(5, data['rate'] - 5)
            stdscr.timeout(data['rate'])
            title_start = time()
        elif key == ord('n'):
            mode = cycle(mode, len(modes) - 1)
            data = init[modes[mode]](maxx, maxy)
            stdscr.timeout(data['rate'])
            start, title_start = time(), time()

        stdscr.erase()

        # draw screen
        update[modes[mode]](data, stdscr)
        if time() - title_start < 2:
            draw_str(data['title'], 1, 1, stdscr)
            draw_str(f'Frame duration: {data["rate"]}', 3, 1, stdscr)

        stdscr.refresh()

        frame_count += 1


if __name__ == "__main__":
    curses.wrapper(main)
