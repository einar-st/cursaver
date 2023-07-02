import curses


def draw_str(str, y, x, stdscr):
    stdscr.addstr(y, x, str)


def draw_ch(ch, y, x, stdscr, col=0):
    try:
        stdscr.addch(y, x, ch, curses.color_pair(col))
    except curses.error:  # bypass error when drawing in bottom right corner
        pass


def wrap(x, y, maxx, maxy):
    if x == maxx:
        x = 0
    elif x == -1:
        x += maxx
    if y == maxy:
        y = 0
    elif y == -1:
        y += maxy

    return xy2i(x, y, maxx)


def cycle(i, max):
    i += 1
    if i > max:
        return 0
    else:
        return i


def i2y(i, maxx):
    return int(i / maxx)


def i2x(i, maxx):
    return int(i % maxx)


def xy2i(x, y, maxx):
    return x + y * maxx
