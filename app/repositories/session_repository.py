import json
from datetime import datetime
from typing import Optional, Dict
from infra.redis_client import redis_client
from lib.auth import REFRESH_TOKEN_EXPIRE_DAYS

class SessionRepository:
    def create_device_session(self, user_id: int, refresh_token: str, device_name: str, ip_address: str):
        """새 기기 세션 생성"""
        session_data = {
            "user_id": user_id,
            "device_name": device_name or "Unknown Device",
            "ip_address": ip_address,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        
        ttl = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
        redis_client.setex(f"refresh:{refresh_token}", ttl, json.dumps(session_data))
        redis_client.sadd(f"user_devices:{user_id}", refresh_token)
        
        return refresh_token
    
    def get_device_session(self, refresh_token: str) -> Optional[Dict]:
        """Refresh Token으로 세션 조회"""
        session_data = redis_client.get(f"refresh:{refresh_token}")
        if not session_data:
            return None
        return json.loads(session_data)
    
    def update_last_activity(self, refresh_token: str):
        """마지막 활동 시간 업데이트"""
        session_data = self.get_device_session(refresh_token)
        if not session_data:
            return False
        
        session_data["last_activity"] = datetime.now().isoformat()
        ttl = redis_client.ttl(f"refresh:{refresh_token}")
        if ttl > 0:
            redis_client.setex(f"refresh:{refresh_token}", ttl, json.dumps(session_data))
        return True
    
    def revoke_device_session(self, user_id: int, refresh_token: str):
        """특정 기기 세션 무효화"""
        redis_client.delete(f"refresh:{refresh_token}")
        redis_client.srem(f"user_devices:{user_id}", refresh_token)
    
    def revoke_all_user_sessions(self, user_id: int):
        """사용자의 모든 세션 무효화"""
        device_tokens = redis_client.smembers(f"user_devices:{user_id}")
        
        for refresh_token in device_tokens:
            redis_client.delete(f"refresh:{refresh_token}")
        
        redis_client.delete(f"user_devices:{user_id}")
    
    def get_user_devices(self, user_id: int):
        """사용자의 모든 활성 기기 조회"""
        device_tokens = redis_client.smembers(f"user_devices:{user_id}")
        devices = []
        
        for refresh_token in device_tokens:
            session_data = self.get_device_session(refresh_token)
            if session_data:
                devices.append({
                    "refresh_token": refresh_token,
                    "device_name": session_data["device_name"],
                    "last_active": datetime.fromisoformat(session_data["last_activity"]),
                    "ip_address": session_data["ip_address"],
                    "created_at": datetime.fromisoformat(session_data["created_at"])
                })
            else:
                # 만료된 토큰은 사용자 기기 목록에서 제거
                redis_client.srem(f"user_devices:{user_id}", refresh_token)
        
        return devices

session_repository = SessionRepository()