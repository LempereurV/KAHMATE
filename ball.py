from constants import *


class Ball:
    def __init__(self, init_position):
        self._pos = [init_position, Constants.number_of_columns // 2 + 1]
        self._carrier = None

    def is_carried(self):
        return self._carrier != None

    def set_carrier(self, rugbyman):
        self._carrier = rugbyman

    def get_pos(self):
        return self._pos

    def get_pos_x(self):
        return self._pos[0]

    def get_pos_y(self):
        return self._pos[1]

    def get_carrier(self):
        if self.is_carried():
            return self._carrier()
        else:
            return False

    def set_pos(self, position):
        self._pos = position

    def left(self):
        self._carrier = None

    def moved(self, position):
        self._position = position
