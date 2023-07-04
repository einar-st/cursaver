# todo
# - loop detection

import curses
from funcs import draw_ch, draw_str, cycle, wrap, i2y, i2x
import random


def count_neighbors(cell, cells, maxx, maxy):

    x, y = i2x(cell, maxx), i2y(cell, maxx)

    neighbors = [
        wrap(x - 1, y - 1, maxx, maxy),
        wrap(x, y - 1, maxx, maxy),
        wrap(x + 1, y - 1, maxx, maxy),
        wrap(x - 1, y, maxx, maxy),
        wrap(x + 1, y, maxx, maxy),
        wrap(x - 1, y + 1, maxx, maxy),
        wrap(x, y + 1, maxx, maxy),
        wrap(x + 1, y + 1, maxx, maxy),
    ]

    count = 0
    for neighbor in neighbors:
        count += min(1, cells[neighbor])

    return count


def gol_init(maxx, maxy):

    data = {}
    data['title'] = 'Game of Life'
    data['maxx'] = maxx
    data['maxy'] = maxy
    data['rate'] = 60

    data['snaps'] = [[], []]
    data['snap_idx'] = 0
    data['snap_cnt'] = 0

    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)

    data['cells'] = [random.randint(0, 1) for _ in range(maxx * maxy)]
    return data


def gol_update(data, stdscr):

    maxx = data['maxx']
    maxy = data['maxy']
    cells = data['cells']
    flip_queue = []

    # repopulate if in closed loop
    if data['snap_cnt'] == 15:  # snapshot every 15th iteration
        data['snaps'][data['snap_idx']] = cells.copy()
        data['snap_idx'] = cycle(data['snap_idx'], 1)
        if data['snaps'][0] == data['snaps'][1]:
            data['cells'] = [random.randint(0, 1) for _ in range(maxx * maxy)]
        data['snap_cnt'] = 0
    else:
        data['snap_cnt'] += 1

    # add cells to flip-queue and draw live cells
    for cell in range(maxx * maxy):
        count = count_neighbors(cell, cells, maxx, maxy)

        x = i2x(cell, maxx)
        y = i2y(cell, maxx)

        if cells[cell] >= 1 and (count == 2 or count == 3):
            if cells[cell] == 1:
                draw_ch('#', y, x, stdscr, 1)
                cells[cell] += 1
            else:
                draw_ch('#', y, x, stdscr)
        elif (
            (cells[cell] >= 1 and (count < 2 or count > 3))
            or (cells[cell] == 0 and count == 3)
        ):
            flip_queue.append(cell)
            if cells[cell] > 1:
                draw_ch('#', y, x, stdscr, 2)
            elif cells[cell] == 1:
                draw_ch('#', y, x, stdscr, 1)

    # flip cells
    for cell in flip_queue:
        if cells[cell] >= 1:
            cells[cell] = 0
        else:
            cells[cell] = 1
