class Field:
    letters = [chr(i) for i in range(ord('A'), ord('J') + 1)]

    def __init__(self, sz):
        self.size = sz
        self.map = [[' ' for _ in range(sz)] for _ in range(sz)]
        self.radar = [[' ' for _ in range(sz)] for _ in range(sz)]

    def get_field_part(self, elem):
        if elem == 'map':
            return self.map
        if elem == 'radar':
            return self.radar

    def draw_field(self, elem):
        field = self.get_field_part(elem)
        for i in range(-1, self.size):
            for j in range(-1, self.size):
                if i == -1 and j == -1:
                    print('  ', end='')
                    continue
                if i == -1:
                    print(j + 1, end=' ')
                    continue
                if j == -1:
                    print(Field.letters[i], end='')
                    continue
                print(' ' + str(field[i][j]), end='')
            print()
        print()

    def check_ship_fits(self, ship, element):
        field = self.get_field_part(element)
        if not (
                0 <= ship.x <= ship.x + ship.height - 1 < self.size and 0 <= ship.y <= ship.y + ship.width - 1 < self.size):
            return False
        x, y, width, height = ship.x, ship.y, ship.width, ship.height

        for i in range(x, x + height):
            for j in range(y, y + width):
                if str(field[i][j]) == '•':
                    return False

        for i in range(x - 1, x + height + 1):
            for j in range(y - 1, y + width + 1):
                if 0 <= i < len(field) and 0 <= j < len(field):
                    if str(field[i][j]) in ('■', 'X'):
                        return False
        return True

    def mark_destroyed_ship(self, ship, elem):
        field = self.get_field_part(elem)
        x, y, width, height = ship.x, ship.y, ship.width, ship.height
        for i in range(x - 1, x + height + 1):
            for j in range(y - 1, y + width + 1):
                if 0 <= i < len(field) and 0 <= j < len(field):
                    field[i][j] = '•'

        for i in range(x, x + height):
            for j in range(y, y + width):
                field[i][j] = 'X'

    def add_ship_to_field(self, ship, elem):
        field = self.get_field_part(elem)
        x, y, width, height = ship.x, ship.y, ship.width, ship.height
        for i in range(x, x + height):
            for j in range(y, y + width):
                field[i][j] = ship
