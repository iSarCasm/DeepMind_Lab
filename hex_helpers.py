from functools import lru_cache

@lru_cache(maxsize=None)
def nearest_neighbours(x, y, size):
    neighbours = []
    width = size
    height = size

    if x+1 < width:
        neighbours.append((x+1, y))
    if x-1 >= 0:
        neighbours.append((x-1, y))
    if(y % 2 == 1):
        if y - 1 >= 0:
            neighbours.append((x, y-1))
        if y -1 >= 0 and x + 1 < width:
            neighbours.append((x+1, y-1))
        if y + 1 < height:
            neighbours.append((x, y+1))
        if x + 1 < width and y + 1 < height:
            neighbours.append((x+1, y+1))
    else:
        if y-1 >= 0 and x-1 > 0:
            neighbours.append((x-1, y-1))
        if y-1 >= 0:
            neighbours.append((x, y-1))
        if x-1 >= 0 and y+1 < height:
            neighbours.append((x-1, y+1))
        if y+1 < height:
            neighbours.append((x, y+1))
    return neighbours

@lru_cache(maxsize=None)
def neighbours(x, y, size, dist=1, remove_start=True):
    neighbours = set([(x, y)])
    for i in range(dist):
        for c1 in list(neighbours):
            temp = nearest_neighbours(c1[0], c1[1], size)
            for c2 in temp:
                neighbours.add(c2)

    if remove_start:
        neighbours.remove((x, y))

    return neighbours

def player_cells(player, board):
    cells = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == player:
                cells.append((x, y, board[y][x]))
    return cells

def available_cells(cells, board):
    return list(filter(lambda cell: board[cell[1]][cell[0]] == 0, cells))