from random import choice, randint

def get_rendom_bool(r, mxr):
    t = randint(0, mxr)
    return t <= r
    

def get_rendom_cell(w, h):
    return (randint(0, w - 1), randint(0, h - 1))

# 0 - up, 1 - right, 2 - down, 3 - left
def get_random_cell2(x, y, w, h):
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dx, dy = choice(moves)
    new_x = max(0, min(x + dx, w - 1))
    new_y = max(0, min(y + dy, h - 1))

    return new_x, new_y
