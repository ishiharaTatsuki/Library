# 二次元配列斜め操作
N = 8
def is_safe(board, row, col):
    for i in range(N):
        if board[row][i] == "Q":
            return False
    # 始点から左斜め上
    for i, j in zip(range(row, - 1, -1), range(col, - 1, -1)):
        if board[i][j] == "Q":
            return False
    # 始点から右斜め上
    for i, j in zip(range(row, - 1, -1), range(col, N)):
        if board[i][j] == "Q":
            return False
    # 始点から左斜め下
    for i, j in zip(range(row, N), range(col, -1, -1)):
        if board[i][j] == "Q":
            return False
    # 始点から右斜め下
    for i, j in zip(range(row, N), range(col, N)):
        if board[i][j] == "Q":
            return False
    return True