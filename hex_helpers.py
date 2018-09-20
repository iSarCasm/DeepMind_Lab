from functools import lru_cache

@lru_cache(maxsize=64000)
def nearest_neighbours(x, y, board):
    neighbours = []
    width = len(board[0])
    height = len(board)

    if x+1 < width:
        neighbours.append((x+1, y, board[y][x+1]))
    if x-1 >= 0:
        neighbours.append((x-1, y, board[y][x-1]))
    if(y % 2 == 1):
        if y - 1 >= 0:
            neighbours.append((x, y-1, board[y-1][x]))
        if y -1 >= 0 and x + 1 < width:
            neighbours.append((x+1, y-1, board[y-1][x+1]))
        if y + 1 < height:
            neighbours.append((x, y+1, board[y+1][x]))
        if x + 1 < width and y + 1 < height:
            neighbours.append((x+1, y+1, board[y+1][x+1]))
    else:
        if y-1 >= 0 and x-1 > 0:
            neighbours.append((x-1, y-1, board[y-1][x-1]))
        if y-1 >= 0:
            neighbours.append((x, y-1, board[y-1][x]))
        if x-1 >= 0 and y+1 < height:
            neighbours.append((x-1, y+1, board[y+1][x-1]))
        if y+1 < height:
            neighbours.append((x, y+1, board[y+1][x]))
    print(nearest_neighbours.cache_info())
    return neighbours

# @lru_cache(maxsize=64000)
def neighbours(x, y, board, dist=1, remove_start=True):
    neighbours_set = set([(x, y, board[y][x])])
    for i in range(dist):
        for c1 in list(neighbours_set):
            temp = nearest_neighbours(c1[0], c1[1], board)
            for c2 in temp:
                neighbours_set.add(c2)

    if remove_start:
        neighbours_set.remove((x, y, board[y][x]))

    # print(neighbours.cache_info())
    return neighbours_set

@lru_cache(maxsize=64000)
def player_cells(player, board):
    cells = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == player:
                cells.append((x, y, board[y][x]))
    return cells

def available_cells(cells):
    return list(filter(lambda cell: cell[2] == 0, cells))
