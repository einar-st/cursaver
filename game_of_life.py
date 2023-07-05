# Todo:
# - enable/disable wrap

import curses
from funcs import draw_ch, draw_str, cycle, wrap, i2y, i2x, xy2i
import random
from time import time


def draw_grid(coords, maxx, maxy):

    cells = [0 for _ in range(maxx * maxy)]

    for x, y in coords:
        cells[xy2i(x, y, maxx)] = 1

    return cells


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
    data['rate'] = 100

    data['snaps'] = [[], []]
    data['snap_idx'] = 0
    data['snap_cnt'] = 0

    data['lmode'] = 0
    # data['lmodes'] = [None, 'glider', 'light']
    data['start_lmode'] = time()
    data['change_mode'] = False

    data['shapes'] = [
        None,
        {
            'name': 'Glider',
            'state': [
                (4, 5),
                (5, 5),
                (6, 5),
                (6, 4),
                (5, 3)
            ]
        },
        {
            'name': 'Light ship',
            'state': [
                (1, int(maxy / 2 - 3)),
                (1, int(maxy / 2 - 1)),
                (2, int(maxy / 2)),
                (3, int(maxy / 2)),
                (4, int(maxy / 2)),
                (5, int(maxy / 2)),
                (5, int(maxy / 2 - 1)),
                (5, int(maxy / 2 - 2)),
                (4, int(maxy / 2 - 3)),
            ]
        }
    ]

    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)

    data['cells'] = [random.randint(0, 1) for _ in range(maxx * maxy)]

    return data


def gol_update(data, stdscr):

    maxx = data['maxx']
    maxy = data['maxy']
    flip_queue = []
    # ch = '\uf111'
    ch = '#'

    # repopulate if in closed loop
    if data['lmode'] == 0:
        if data['snap_cnt'] == 15:  # snapshot every 15th iteration
            data['snaps'][data['snap_idx']] = data['cells'].copy()
            data['snap_idx'] = cycle(data['snap_idx'], 1)
            if data['snaps'][0] == data['snaps'][1]:
                data['snaps'] = [[], []]
                data['cells'] = [
                    random.randint(0, 1) for _ in range(maxx * maxy)
                ]
            data['snap_cnt'] = 0
        else:
            data['snap_cnt'] += 1

    # change mode
    if data['change_mode']:
        data['lmode'] = cycle(data['lmode'], 2)
        if data['lmode'] != 0:
            data['cells'] = draw_grid(
                data['shapes'][data['lmode']]['state'], maxx, maxy
            )
        else:
            data['cells'] = [random.randint(0, 1) for _ in range(maxx * maxy)]
        data['start_lmode'] = time()
        data['change_mode'] = False

    cells = data['cells']

    # add cells to flip-queue and draw live cells
    for cell in range(maxx * maxy):
        count = count_neighbors(cell, cells, maxx, maxy)

        x = i2x(cell, maxx)
        y = i2y(cell, maxx)

        if cells[cell] >= 1 and (count == 2 or count == 3):
            if cells[cell] == 1:
                draw_ch(ch, y, x, stdscr, 1)
                cells[cell] += 1
            else:
                draw_ch(ch, y, x, stdscr)
        elif (
            (cells[cell] >= 1 and (count < 2 or count > 3))
            or (cells[cell] == 0 and count == 3)
        ):
            flip_queue.append(cell)
            if cells[cell] > 1:
                draw_ch(ch, y, x, stdscr, 2)
            elif cells[cell] == 1:
                draw_ch(ch, y, x, stdscr, 1)

    # flip cells
    for cell in flip_queue:
        if cells[cell] >= 1:
            cells[cell] = 0
        else:
            cells[cell] = 1

    if time() - data['start_lmode'] < 2 and data['lmode'] != 0:
        draw_str(data['shapes'][data['lmode']]['name'], 2, 1, stdscr)
