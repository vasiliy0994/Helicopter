from utils import get_rendom_bool

class Clouds:
    def __init__(self,w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for _ in range(self.w)] for _ in range(self.h)]

    def update(self, r = 1, mxr = 20, g = 1, mxg = 20):
        for i in range(self.w):
            for j in range(self.h):
                if get_rendom_bool(r, mxr):
                    self.cells[i][j] = 1
                    if get_rendom_bool(g, mxg):
                        self.cells[i][j] = 2
                else:
                    self.cells[i][j] = 0

    def export_data(self):
        return {'cells': self.cells}
    
    def import_data(self, data):
        self.cells = data['cells'] or [[0 for _ in range(self.w)] for _ in range(self.h)]
