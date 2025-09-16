import typer
from commands import board_command, session_command

app = typer.Typer()
app.add_typer(board_command.app, name="board")
app.add_typer(session_command.app, name="session")

if __name__ == "__main__":
    app()