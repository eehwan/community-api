from typing import Optional
from infra.redis_client import redis_client
from lib.auth import ACCESS_TOKEN_EXPIRE_MINUTES

class SessionRepository:
    def store_session(self, user_id: int, token: str):
        redis_client.setex(f"session:{user_id}", ACCESS_TOKEN_EXPIRE_MINUTES * 60, token)
    
    def get_session(self, user_id: int) -> Optional[str]:
        return redis_client.get(f"session:{user_id}")
    
    def delete_session(self, user_id: int):
        redis_client.delete(f"session:{user_id}")

session_repository = SessionRepository()