from .games import minesweeper

games = {
    minesweeper.name():minesweeper.factory()
}