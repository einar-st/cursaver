import curses
import random
from funcs import draw_ch, draw_str, i2y, i2x, cycle
from time import time

# Todo:
# - Indicators on bottom


def sel_sort(nums):

    for i in range(len(nums) - 1):
        low = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[low]:
                low = j
            vars = {low: 3, i: 2, j: 1}
            yield (nums, vars)
        nums[i], nums[low] = nums[low], nums[i]

    start = time()
    while time() - start < 2:
        yield nums, {}


def bubble_sort(nums):

    for i in range(len(nums) - 1):
        for x in range(len(nums) - 1 - i):
            y = x + 1
            if nums[x] > nums[y]:
                nums[x], nums[y] = nums[y], nums[x]
            vars = {y: 1, x: 2}
            yield nums, vars

    start = time()
    while time() - start < 2:
        yield nums, {}


def insert_sort(nums):

    for x in range(1, len(nums)):
        for i in range(x, -1, -1):
            vars = {i: 2, x: 3}
            yield nums, vars
            if i == 0 or nums[i] > nums[i-1]:
                break
            else:
                nums[i], nums[i-1] = nums[i-1], nums[i]

    start = time()
    while time() - start < 2:
        yield nums, {}


def quick_sort(nums, top=True, *args):

    try:
        lo, hi = args[0]
    except IndexError:
        lo = 0
        hi = len(nums) - 1

    if lo >= hi:
        return

    j = lo - 1
    p = hi

    # middle of three
    mot = [nums[lo], nums[int(len(nums) / 2)], nums[hi]]
    mot.remove(min(mot))
    mot.remove(max(mot))
    for i in (lo, int(len(nums) / 2)):
        if nums[i] == mot[0]:
            nums[i], nums[p] = nums[p], nums[i]
            break

    for i in range(lo, hi):
        if nums[i] < nums[p]:
            j += 1
            nums[i], nums[j] = nums[j], nums[i]
        yield nums, {lo: 2, i: 3, j: 3, p: 1}

    nums[p], nums[j+1] = nums[j+1], nums[p]

    for res in quick_sort(nums, False, (lo, j)):
        yield res

    for res in quick_sort(nums, False, (j + 2, hi)):
        yield res

    if top:
        yield nums, {}


def sort_init(maxx, maxy):

    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)

    data = {}
    data['title'] = 'Sorting algorithms'
    data['maxx'] = maxx
    data['maxy'] = maxy
    data['rate'] = 20
    data['algs'] = (sel_sort, bubble_sort, insert_sort, quick_sort)
    data['alg_names'] = (
        'Selection sort',
        'Bubble sort',
        'Insert sort',
        'Quick sort'
    )
    data['alg'] = 0
    data['start_alg'] = time()
    data['change_mode'] = False

    nums = []
    for i in range(maxx):
        nums.append(random.randrange(1, maxy))

    data['nums'] = data['algs'][data['alg']](nums)

    return data


def sort_update(data, stdscr):

    maxx = data['maxx']
    maxy = data['maxy']
    alg = data['alg']
    algs = data['algs']
    alg_names = data['alg_names']

    try:
        nums, vars = next(data['nums'])
    except StopIteration:
        data['change_mode'] = True

    if data['change_mode']:
        nums = []
        vars = {}
        data['alg'] = cycle(alg, len(algs) - 1)
        for i in range(maxx):
            nums.append(random.randrange(1, maxy))
        data['nums'] = algs[data['alg']](nums)
        data['start_alg'] = time()
        data['change_mode'] = False

    for pos in range(1, maxx * maxy):
        x = i2x(pos, maxx)
        y = i2y(pos, maxx)
        if nums[x] >= maxy - y:
            if x in vars.keys():
                draw_ch('|', y, x, stdscr, vars[x])
            else:
                draw_ch('#', y, x, stdscr)

    if time() - data['start_alg'] < 2:
        draw_str(alg_names[alg], 2, 1, stdscr)
