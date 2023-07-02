import curses
import random
from funcs import draw_ch, i2y, i2x, xy2i, cycle
from time import time


def sel_sort(nums):

    # start = time()
    # while time() - start < 2:
    #     vars = {}
    #     yield (nums, vars)

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
        vars = {}
        yield (nums, vars)


def bubble_sort(nums):

    # start = time()
    # while time() - start < 2:
    #     vars = {}
    #     yield (nums, vars)

    for i in range(len(nums) - 1):
        for x in range(len(nums) - 1 - i):
            y = x + 1
            if nums[x] > nums[y]:
                nums[x], nums[y] = nums[y], nums[x]
            vars = {y: 1, x: 2}
            yield nums, vars

    start = time()
    while time() - start < 2:
        vars = {}
        yield (nums, vars)


def sort_init(maxx, maxy):

    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)

    data = {}
    data['title'] = 'Sorting algorithms'
    data['maxx'] = maxx
    data['maxy'] = maxy
    data['ant'] = xy2i(int(maxx/2), int(maxy/2), maxx)
    data['direction'] = 0
    data['algs'] = [sel_sort, bubble_sort]
    data['alg'] = 0

    nums = []
    for i in range(maxx):
        nums.append(random.randrange(1, maxy))

    data['nums'] = data['algs'][data['alg']](nums)

    return data


def sort_update(data, stdscr):

    maxx = data['maxx']
    maxy = data['maxy']

    try:
        nums, vars = next(data['nums'])
    except StopIteration:
        nums = []
        vars = {}
        data['alg'] = cycle(data['alg'], len(data['algs']) - 1)
        for i in range(maxx):
            nums.append(random.randrange(1, maxy))
        data['nums'] = data['algs'][data['alg']](nums)

    for pos in range(1, maxx * maxy):
        x = i2x(pos, maxx)
        y = i2y(pos, maxx)
        if nums[x] >= maxy - y:
            if x in vars.keys():
                draw_ch('|', y, x, stdscr, vars[x])
            else:
                draw_ch('#', y, x, stdscr)
