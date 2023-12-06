

class Ball:
    def __init__(self, init_position):
        self._position = [init_position, 5]
        self._carrier = None

    def is_carried(self):
        return self._carrier != None

    def set_carrier(self, rugbyman):
        self._carrier = rugbyman

    def get_position(self):
        return self._position
    
    def get_position_x(self):
        return self._position[0]

    def get_position_y(self):
        return self._position[1]
    
    def get_carrier(self):
        if self.is_carried():
            return self._carrier()
        else :
            return False
    
    
    def set_position(self, position):
        self._position = position
    
    def left(self):
        self._carrier = None

    def moved(self, position):
        self._position = position