import curses
from funcs import draw_ch, wrap, i2y, i2x, xy2i


def ant_init(maxx, maxy):

    data = {}
    data['maxx'] = maxx
    data['title'] = 'Langton\'s Ant'
    data['maxy'] = maxy
    data['ant'] = xy2i(int(maxx/2), int(maxy/2), maxx)
    data['cells'] = []
    data['direction'] = 0

    for i in range(maxx * maxy):
        data['cells'].append(0)

    return data


def ant_update(data, stdscr):

    ant = data['ant']  # ant index
    cells = data['cells']
    maxx, maxy = data['maxx'], data['maxy']

    # flip cell for cell below ant
    cells[ant] = not cells[ant]

    # change direction
    if cells[ant]:
        if data['direction'] < 3:
            data['direction'] += 1
        else:
            data['direction'] = 0
    if not cells[ant]:
        if data['direction'] > 0:
            data['direction'] -= 1
        else:
            data['direction'] = 3

    direction = data['direction']

    # advance
    x = i2x(data['ant'], maxx)
    y = i2y(data['ant'], maxx)

    if direction == 0:
        x -= 1
    elif direction == 1:
        y -= 1
    elif direction == 2:
        x += 1
    elif direction == 3:
        y += 1

    data['ant'] = wrap(x, y, maxx, maxy)

    for i, cell in enumerate(cells):
        if cell == 1:
            try:
                draw_ch('#', i2y(i, maxx), i2x(i, maxx), stdscr, 0)
            except curses.error:
                pass

        draw_ch('*', i2y(data['ant'], maxx), i2x(data['ant'], maxx), stdscr, 0)
