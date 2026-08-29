# reallab3

This project is a Flask-based web application for a simple online Minesweeper game. It serves the game UI from the `games/` folder, tracks active game sessions in memory, and exposes endpoints for login, game creation, and board interactions.

## Project structure

- `app.py` – Flask application entry point and game API routes
- `minesweeperGame.py` – standalone command-line Minesweeper prototype
- `requirements.txt` – Python package dependencies
- `static/` – static web assets, including HTML pages and error page
- `games/minesweeper/` – Minesweeper game assets and templates

## Features

- User login and registration endpoints
- Dynamic game session creation using unique IDs
- Minesweeper board actions (`board`, `pick`, `space`, `name`, `score`, `time`)
- SSE-style stream endpoint for game updates
- Static HTML pages for login and game UI

## Requirements

- Python 3.x
- Flask
- Redis server (used by the app when available for pub/sub streaming)

## Setup

1. Open a terminal in the project directory.
2. Create and activate a virtual environment if needed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start Redis locally if you want full streaming support.

## Run the app

```bash
python app.py
```

The app runs on port `8080` by default.

Open the browser to:

- `http://localhost:8080/login`
- or a game route such as `http://localhost:8080/games/minesweeper`

## Notes

- If Redis is not running, the server will print an error message but may still start partially for non-streamed behavior.
- The game logic itself is in the `games/minesweeper` package, and the main web application routes connect to it from `app.py`.
- The root `minesweeperGame.py` file is a console version of the Minesweeper game and can be used as a local prototype.

## License

This project is provided as coursework/demo code and is intended for educational use.
