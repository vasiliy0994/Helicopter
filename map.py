from utils import get_rendom_bool
from utils import get_rendom_cell
from utils import get_random_cell2


# 0 - поле
# 1 - дерево
# 2 - река
# 3 - госпиталь
# 4 - апгрейт шоп
# 5 - огонь

CELL_TYIPS = '🟩🌲🌊🏥🏦🔥'
TREE_BONUS = 100
UPGRADE_COST = 500
LIFE_COST = 100


class Map:
    CELL_TYIPS = '🟩🌲🌊🏥🏦🔥'
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for _ in range(self.w)] for _ in range(self.h)]
        self.generate_forest(2,10)
        self.generate_river(100)
        self.generate_river(100)
        self.generate_upgrade_shop()
        self.generate_hospital()

    def check_bounds(self, x, y):
        if x < 0 or y < 0 or x > self.w or y > self.h:
            return False
        return True
    
    def print_map(self, helico, clouds):
        print('⬛️' * (self.w + 2))
        for ri in range(self.h):
            print('⬛️', end='')
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if clouds.cells[ri][ci] == 1:
                    print('⚪️', end='')
                elif clouds.cells[ri][ci] == 2:
                    print('🔵', end='')
                elif helico.x == ri and helico.y == ci:
                    print('🚁', end='')
                elif 0 <= cell < len(self.CELL_TYIPS):
                    print(CELL_TYIPS[cell], end='')
            print('⬛️')
        print('⬛️' * (self.w + 2))

    def generate_river(self, l):
        rc = get_rendom_cell(self.w, self.h)
        rx, ry = rc[0], rc[1]
        if not self.check_bounds(rx, ry):
            return
        self.cells[rx][ry] = 2
        while l > 0:
            rc2 = get_random_cell2(rx, ry, self.w, self.h)
            rx2, ry2 = rc2[0], rc2[1]
            if self.check_bounds(rx2, ry2):
                self.cells[rx2][ry2] = 2
                rx, ry = rx2, ry2
                l -= 1
            else:
                continue

    def generate_upgrade_shop(self):
        c = get_rendom_cell(self.w, self.h)
        cx, cy = c[0], c[1]
        self.cells[cx][cy] = 4

    def generate_hospital(self):
        c = get_rendom_cell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] != 4:
            self.cells[cx][cy] = 3
        else:
            self.generate_hospital()

    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if get_rendom_bool(r, mxr):
                    self.cells[ri][ci] = 1

    def generate_free(self):
        c = get_rendom_cell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.check_bounds(cx, cy) and self.cells[cx][cy] == 0:
            self.cells[cx][cy] = 1

    def add_fire(self):
        c = get_rendom_cell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 5

    def update_fires(self):
        for ri in range(self.w):
            for ci in range(self.h):
                cell = self.cells[ri][ci]
                if cell == 5:
                    self.cells[ri][ci] = 0

        for i in range(10):
            self.add_fire()

    def process_helicopter(self, helico, clouds):
        c = self.cells[helico.x][helico.y]
        d = clouds.cells[helico.x][helico.y]
        if c == 2:
            helico.tank = helico.mxtank
        if c == 5 and helico.tank > 0:
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.x][helico.y] = 1
        if c == 4 and helico.score >= UPGRADE_COST:
            helico.mxtank += 1
            helico.score -= UPGRADE_COST
        if c == 3 and helico.score >= LIFE_COST:
            helico.lives += 1
            helico.score -= LIFE_COST
        if d == 2:
            helico.lives -= 1
            if helico.lives == 0:
                helico.game_over()

    def export_data(self):
        return {'cells': self.cells}
    
    def import_data(self, data):
        self.cells = data['cells'] or [[0 for _ in range(self.w)] for _ in range(self.h)]
