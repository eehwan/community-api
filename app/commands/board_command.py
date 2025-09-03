import typer
from infra.database import SessionLocal
from repositories.board_repository import board_repository

app = typer.Typer()

@app.command()
def syncwithredis():
    """Redis 증감량을 읽어서 게시판 post_count 동기화"""
    db = SessionLocal()
    try:
        deltas = board_repository.get_all_post_count_deltas()
        if not deltas:
            typer.echo("No post count changes to sync")
            return
            
        board_repository.update_board_post_counts(db)
        typer.echo(f"Successfully synced post counts for {len(deltas)} boards")
        
    except Exception as e:
        typer.echo(f"Error during post count sync: {e}", err=True)
        db.rollback()
        raise typer.Exit(1)
    finally:
        db.close()