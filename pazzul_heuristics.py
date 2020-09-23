# 隣接リスト
def create_adjacent(h, w):
    adjacent = [[] for _ in range(h * w)]
    for i in range(h * w):
        if i % w != w - 1:
            adjacent[i].append(i + 1)
        if i % w != 0:
            adjacent[i].append(i - 1)
        if i // h < h - 1:
            adjacent[i].append(i + w)
        if i // h > 0:
            adjacent[i].append(i - w)
    return adjacent


def create_distance(h, w):
    distance = [[0] * h * w for _ in range(h * w)]
    for i in range(h * w):
        if i == 0:
            continue
        ye, xe = divmod(i - 1, w)
        for j in range(h * w):
            y, x = divmod(j, w)
            distance[i][j] = abs(ye - y) + abs(xe - x)
    return distance


def get_distance(board, distance):
    v = 0
    for x in range(len(board)):
        p = board[x]
        if p == 0:
            continue
        v += distance[p][x]
    return v

#
class State1:
    def __init__(self, board, space, prev):
        self.board = board
        self.space = space
        self.prev = prev
        if prev is None:
            self.cost = get_distance(board)
        else:
            p = board[prev.space]
            self.cost = prev.cost - distance[p][space] + distance[p][prev.space]

    def __cmp__(self, x, y):
        return x.cost - y.cost
    #プライオリティーQ使用時、比較する為
    def __lt__(self, other):
        return self.cost < other.cost

# リスト : 山登り法
from functools import cmp_to_key
def hill_climb_search(board, space, cost, history):
    def compar_cost(x, y):
        return x[2] - y[2]
    if board == GOAL:
        for x in history:
            print(*x)
        return True
    else:
        buff = []
        for x in adjacent[space]:
            p = board[x]
            b = board[:]
            b[space] = b[x]
            b[x] = 0
            if b in history:
                continue
            c = cost - distance[p][x] + distance[p][space]
            buff.append((b,x,c))
        # コストの小さい局面から選択する
        buff.sort(key=cmp_to_key(compar_cost))
        for b, x, c in buff:
            history.append(b)
            if hill_climb_search(b, x, c, history):
                return True
            history.pop()
    return False

#  最良優先探索
from heapq import heapify, heappush, heappop
def best_first_search(start):
    state = State1(start, start.index(0), None)
    q = [state]
    # heapify(q)
    table = {}
    table[tuple(start)] = True
    while q:
        a = heappop(q)
        for x in adjacent[a.space]:
            b = a.board[:]
            b[a.space] = b[x]
            b[x] = 0
            key = tuple(b)
            if key in table:
                continue
            c = State1(b, x, a)
            if b == GOAL:
                print(c.board)
                return
            heappush(q, c)
            table[key] = True


# 反復深化
def id_search(limit, move, space, lower):
    if move == limit:
        if board == GOAL:
            global count
            count += 1
            print(move)
            exit()
    else:
        for x in adjacent[space]:
            p = board[x]
            if move_piece[move] == p:
                continue
            board[space], board[x] = p, 0
            move_piece[move + 1] = p
            new_lower = lower - distance[p][x] + distance[p][space]

            if new_lower + move <= limit:
                id_search(limit, move + 1, x, new_lower)
            board[space], board[x] = 0, p


############入力データ###########################
GOAL = [1, 2, 3, 4, 5, 6, 7, 8, 0]
board = [int(s) for _ in range(4) for s in input().split()]
move_piece = [None] * 46
adjacent = create_adjacent(4, 4)
distance = create_distance(4, 4)
n = get_distance(board)
