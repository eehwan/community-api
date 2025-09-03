import typer
from commands import board_command

app = typer.Typer()
app.add_typer(board_command.app, name="board")

if __name__ == "__main__":
    app()