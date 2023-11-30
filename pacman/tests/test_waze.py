from pacman.models.maze import Maze, Wall, Fruit, Empty


def assertIs(cell, position, maze):
    assert isinstance(maze.cells[position[0]][position[1]], cell), f"Expected {
        cell} at {position}, got {maze.cells[position[0]][position[1]]}"


def test_init_waze():

    maze = Maze()

    assert maze.shape == (0, 0)


def test_create_maze():

    maze = Maze([
        [Wall(), Wall(), Wall()],
        [Wall(), Empty(), Wall()],
        [Wall(), Wall(), Wall()],
    ])

    assert maze.shape == (3, 3)


def test_create_from_str():

    maze = Maze.from_str("""
        www
        w.w
        www
    """)

    assert maze.shape == (3, 3)
    assertIs(Wall, (0, 0), maze)
    assertIs(Empty, (1, 1), maze)


def test_create_with_no_one_wall():

    maze = Maze.from_str("""
        www
        ..w
        www
    """)

    assert maze.shape == (3, 3)
    assertIs(Wall, (0, 0), maze)
    assertIs(Empty, (1, 1), maze)


def test_create_with_no_wall():

    maze = Maze.from_str("""
        www
        ...
        www
    """)

    assert maze.shape == (3, 3)
    assertIs(Wall, (0, 0), maze)
    assertIs(Empty, (1, 0), maze)
    assertIs(Empty, (1, 1), maze)
    assertIs(Empty, (1, 2), maze)


def test_create_with_fruit():

    maze = Maze.from_str("""
            www
            .f.
            www
        """)

    assert maze.shape == (3, 3)
    assertIs(Wall, (0, 0), maze)
    assertIs(Fruit, (1, 1), maze)
    assertIs(Wall, (2, 2), maze)


def test_a_complex_maze():

    maze = Maze.from_str("""
            wwwww.
            w..fw.
            w..ww.
            ......
            wwwww.
        """)
    assert maze.shape == (5, 6)
    assertIs(Wall, (0, 0), maze)
    assertIs(Empty, (0, 5), maze)
    assertIs(Fruit, (1, 3), maze)
    assertIs(Wall, (2, 4), maze)

