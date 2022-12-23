from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def turn(self, clockwise=True):
        clockwise_order = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        next_i = clockwise_order.index(self) + (1 if clockwise else -1)
        return clockwise_order[next_i % 4]

    @property
    def score(self):
        return self.value


Orientation = Direction


# FACING_SCORE = { symbol: i for i,symbol in enumerate(">v<^") }
DIRECTION_FACING = {
    Direction.UP: "^",
    Direction.RIGHT: ">",
    Direction.DOWN: "v",
    Direction.LEFT: "<",
}


@dataclass
class PositionBounds:
    row: int
    col: int
    row_min: int
    row_max: int
    col_min: int
    col_max: int


@dataclass
class Position:
    row: int
    col: int

    def __hash__(self):
        return (self.row, self.col).__hash__()

    def copy(self):
        return Position(row=self.row, col=self.col)


@dataclass
class CubeFace:
    id: int
    corner_pos: Position
    size: int
    neighbours: Dict[Direction, Tuple["CubeFace", Orientation]] = field(default_factory=dict)

    def get_neighbours_coords_clockwise(self) -> List[Position]:
        neighbours = []
        for row, col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            neighbours.append(
                Position(
                    row=(row * self.size) + self.corner_pos.row,
                    col=(col * self.size) + self.corner_pos.col,
                )
            )
        return neighbours


@dataclass
class Board:
    tiles: List[List[str]]
    bounds: List[List[PositionBounds]]

    def display(self):
        for row in self.tiles:
            print("".join(row))

    def is_open(self, pos: Position):
        return self.tiles[pos.row][pos.col] == "."

    def is_position_in_void(self, pos: Position):
        bounds = self.bounds[pos.row][pos.col]
        return not (bounds.row_min <= pos.row <= bounds.row_max and bounds.col_min <= pos.col <= bounds.col_max)

    def get_cube_face_size(self):
        height, width = len(self.tiles), len(self.tiles[0])
        return max(height, width) // 4

    def get_start_pos(self):
        bound = self.bounds[0][0]
        return Position(row=0, col=bound.col_min)

    def build_cube_map(self):
        face_size = self.get_cube_face_size()
        faces = {}
        for i, region_corner in enumerate(self.iter_region_corners()):
            face = CubeFace(id=i, corner_pos=region_corner, size=face_size)
            faces[region_corner] = face

            for pos, dir in zip(
                face.get_neighbours_coords_clockwise(), (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)
            ):
                if pos not in faces:
                    continue
                other_face = faces[pos]
                face.neighbours[dir] = (other_face, Direction.UP)
                other_face.neighbours[dir.turn().turn()] = (face, Direction.UP)

        for _ in range(4):
            self.fold_faces(faces)
        self.cube_faces = faces

    #      |
    #  C---+---A
    #      |
    #      B
    def fold_faces(self, faces: Dict[Position, CubeFace]):
        connections_remaining = 6 * 4
        for face in faces.values():
            connections_remaining -= len(face.neighbours)
            dir1, dir2 = Direction.RIGHT, Direction.UP
            for _ in range(4):
                dir1 = dir1.turn()
                dir2 = dir2.turn()
                if dir1 in face.neighbours and dir2 in face.neighbours:
                    face1, orientation1 = face.neighbours[dir1]
                    face2, orientation2 = face.neighbours[dir2]

                    # rotate -num of turns to make upright
                    slot1 = dir1.turn().turn().turn()
                    slot2 = dir2.turn().turn().turn(clockwise=False)
                    x1 = orientation1
                    x2 = orientation2
                    while x1 != Direction.UP:
                        slot1 = slot1.turn()
                        x1 = x1.turn()
                    while x2 != Direction.UP:
                        slot2 = slot2.turn()
                        x2 = x2.turn()

                    o1 = orientation1
                    o2 = orientation2
                    orientation2 = orientation2.turn()
                    while o1 != Direction.UP:
                        o1 = o1.turn()
                        orientation2 = orientation2.turn()
                    face1.neighbours[slot1] = (face2, orientation2)

                    orientation1 = orientation1.turn(clockwise=False)
                    while o2 != Direction.UP:
                        o2 = o2.turn()
                        orientation1 = orientation1.turn()
                    face2.neighbours[slot2] = (face1, orientation1)

    def print_connections(self, faces: Dict[Position, CubeFace]):
        for pos, face in faces.items():
            print(face.id)
            print(pos)
            print("NEIGHBOURS")
            for dir, face_and_orientation in face.neighbours.items():
                face, orientation = face_and_orientation
                print("DIR:", dir)
                print("Orientation:", orientation)
                print("Face:", face.corner_pos)
            print()

    def fold_faces_old(self, faces: Dict[Direction, CubeFace]):
        connections_remaining = 6 * 4
        for face in faces.values():
            connections_remaining -= len(face.neighbours)
            dir1, dir2 = Direction.UP, Direction.RIGHT
            for _ in range(4):
                dir1 = dir1.turn()
                dir2 = dir2.turn()
                if dir1 in face.neighbours and dir2 in face.neighbours:
                    # Connect two faces that touch only when folding up the cube
                    face1, orientation1 = face.neighbours[dir1]
                    face2, orientation2 = face.neighbours[dir2]

                    face2.neighbours[dir2.turn().turn()] = (face, orientation1.turn())
                    face1.neighbours[dir1.turn().turn()] = (face, orientation2.turn(clockwise=False))

    def iter_region_corners(self):
        # There are 6 regions, each corresponding to the face of a cube
        region_size = self.get_cube_face_size()
        board_width = len(self.tiles[0])

        pos = Position(row=0, col=0)
        corners_left = 6
        while corners_left > 0:
            if not self.is_position_in_void(pos):
                yield pos.copy()
                corners_left -= 1

            pos.col += region_size
            if pos.col // board_width > 0:
                pos.row += region_size
            pos.col %= board_width

    def get_cube_face(self, pos: Position):
        for corner, face in self.cube_faces.items():
            if 0 <= pos.row - corner.row < face.size and 0 <= pos.col - corner.col < face.size:
                return face
        raise ValueError(f"Position {pos} is not on a cube face.")


def rotate_on_face_edge_counterclockwise(pos: Position, face_width: int):
    return Position(row=face_width - 1 - pos.col, col=pos.row)


@dataclass
class Person:
    pos: Position
    direction: Direction

    def next_target_position(self, board: Board):
        curr_row, curr_col = self.pos.row, self.pos.col

        next_pos = Position(row=curr_row, col=curr_col)
        if self.direction == Direction.UP:
            next_pos.row -= 1
        elif self.direction == Direction.DOWN:
            next_pos.row += 1
        elif self.direction == Direction.LEFT:
            next_pos.col -= 1
        elif self.direction == Direction.RIGHT:
            next_pos.col += 1

        bounds = board.bounds[curr_row][curr_col]
        if next_pos.row < bounds.row_min:
            next_pos.row = bounds.row_max
        elif next_pos.row > bounds.row_max:
            next_pos.row = bounds.row_min
        elif next_pos.col < bounds.col_min:
            next_pos.col = bounds.col_max
        elif next_pos.col > bounds.col_max:
            next_pos.col = bounds.col_min

        return next_pos

    def next_target_position_on_cube(self, board: Board):
        curr_row, curr_col = self.pos.row, self.pos.col

        next_pos = Position(row=curr_row, col=curr_col)
        if self.direction == Direction.UP:
            next_pos.row -= 1
        elif self.direction == Direction.DOWN:
            next_pos.row += 1
        elif self.direction == Direction.LEFT:
            next_pos.col -= 1
        elif self.direction == Direction.RIGHT:
            next_pos.col += 1

        current_face = board.get_cube_face(self.pos)
        coords = Position(
            row=next_pos.row - current_face.corner_pos.row,
            col=next_pos.col - current_face.corner_pos.col,
        )
        if coords.row < 0:
            next_face, orientation = current_face.neighbours[Direction.UP]
            new_face_coords = Position(row=next_face.size - 1, col=coords.col)
        elif coords.row >= current_face.size:
            next_face, orientation = current_face.neighbours[Direction.DOWN]
            new_face_coords = Position(row=0, col=coords.col)
        elif coords.col < 0:
            next_face, orientation = current_face.neighbours[Direction.LEFT]
            new_face_coords = Position(row=coords.row, col=next_face.size - 1)
        elif coords.col >= current_face.size:
            next_face, orientation = current_face.neighbours[Direction.RIGHT]
            new_face_coords = Position(row=coords.row, col=0)
        else:
            return next_pos, Direction.UP

        pos = new_face_coords
        change_in_orientation = Direction.UP
        while orientation != Direction.UP:
            pos = rotate_on_face_edge_counterclockwise(pos, next_face.size)
            orientation = orientation.turn(clockwise=False)
            change_in_orientation = change_in_orientation.turn(clockwise=False)

        row, col = next_face.corner_pos.row, next_face.corner_pos.col
        return Position(row + pos.row, col + pos.col), change_in_orientation

    def is_blocked(self, board: Board):
        next_pos = self.next_target_position(board)
        return board.tiles[next_pos.row][next_pos.col] == "#"

    def take_step(self, board: Board):
        if self.is_blocked(board):
            raise RuntimeError("Cannot walk through walls!")
        self.pos = self.next_target_position(board)

    def is_blocked_on_cube(self, board: Board):
        next_pos, _ = self.next_target_position_on_cube(board)
        return board.tiles[next_pos.row][next_pos.col] == "#"

    def take_step_on_cube(self, board: Board):
        if self.is_blocked_on_cube(board):
            raise RuntimeError("Cannot walk through walls!")
        self.pos, change_in_rotation = self.next_target_position_on_cube(board)
        while change_in_rotation != Direction.UP:
            change_in_rotation = change_in_rotation.turn(clockwise=False)
            self.direction = self.direction.turn()


def follow_path(path: str, board: Board):
    pos = board.get_start_pos()
    person = Person(pos=pos, direction=Direction.RIGHT)
    board.tiles[pos.row][pos.col] = DIRECTION_FACING[person.direction]
    for move in iter_moves(path):
        while move:
            if move == "L":
                person.direction = person.direction.turn(clockwise=False)
                move = ""
            elif move == "R":
                person.direction = person.direction.turn(clockwise=True)
                move = ""
            else:
                if not person.is_blocked(board):
                    person.take_step(board)
                    move -= 1
                else:
                    break
            board.tiles[person.pos.row][person.pos.col] = DIRECTION_FACING[person.direction]
    return person.pos, person.direction


def follow_cube_path(path: str, board: Board):
    board.build_cube_map()
    pos = board.get_start_pos()
    person = Person(pos=pos, direction=Direction.RIGHT)
    board.tiles[pos.row][pos.col] = DIRECTION_FACING[person.direction]
    for move in iter_moves(path):
        while move:
            if move == "L":
                person.direction = person.direction.turn(clockwise=False)
                move = ""
            elif move == "R":
                person.direction = person.direction.turn(clockwise=True)
                move = ""
            else:
                if not person.is_blocked_on_cube(board):
                    person.take_step_on_cube(board)
                    move -= 1
                else:
                    break
            board.tiles[person.pos.row][person.pos.col] = DIRECTION_FACING[person.direction]
    return person.pos, person.direction


def get_password(position: Position, direction: Direction):
    row, column = position.row + 1, position.col + 1
    return 1000 * row + 4 * column + direction.score


def iter_moves(moves: str):
    i = 0
    while i < len(moves):
        if moves[i].isdigit():
            j = i
            while j < len(moves) and moves[j].isdigit():
                j += 1
            yield int(moves[i:j])
            i = j
        else:
            yield moves[i]
            i += 1
