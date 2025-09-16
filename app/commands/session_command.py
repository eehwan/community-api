import typer
from datetime import datetime
from infra.database import SessionLocal
from sqlalchemy import and_, or_
from entities.session import Session as SessionModel

app = typer.Typer()

@app.command()
def cleanup():
    """만료된 세션들을 정리합니다 (expires_at 기준)"""
    db = SessionLocal()
    try:
        current_time = datetime.now()
        
        # 인덱스를 효율적으로 사용: expires_at만으로 필터링
        query = db.query(SessionModel).filter(
            SessionModel.expires_at < current_time
        )
        
        count = query.count()
        
        if count == 0:
            typer.echo("정리할 만료된 세션이 없습니다.")
            return
            
        # 실제 삭제 (인덱스를 활용한 효율적인 삭제)
        deleted_count = query.delete(synchronize_session=False)
        db.commit()
        
        typer.echo(f"✅ {deleted_count}개 세션이 성공적으로 정리되었습니다.")
        
    except Exception as e:
        typer.echo(f"❌ 세션 정리 중 오류 발생: {e}", err=True)
        db.rollback()
        raise typer.Exit(1)
    finally:
        db.close()

@app.command()
def stats():
    """세션 통계 정보를 보여줍니다"""
    db = SessionLocal()
    try:
        current_time = datetime.now()
        
        # 전체 세션 수
        total_count = db.query(SessionModel).count()
        
        # 활성 세션 수 (만료되지 않은 세션)
        active_count = db.query(SessionModel).filter(
            SessionModel.expires_at > current_time
        ).count()
        
        # 만료된 세션 수
        expired_count = db.query(SessionModel).filter(
            SessionModel.expires_at < current_time
        ).count()
        
        typer.echo("📊 세션 통계:")
        typer.echo(f"  전체 세션: {total_count}개")
        typer.echo(f"  활성 세션: {active_count}개")
        typer.echo(f"  만료된 세션: {expired_count}개")
        
        if expired_count > 0:
            typer.echo(f"  💡 정리 가능: {expired_count}개 (cleanup 명령어 사용)")
        
    except Exception as e:
        typer.echo(f"❌ 통계 조회 중 오류 발생: {e}", err=True)
        raise typer.Exit(1)
    finally:
        db.close()