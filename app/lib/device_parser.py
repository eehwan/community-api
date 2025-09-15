from user_agents import parse

def parse_device_name(user_agent_string: str) -> str:
    """User-Agent를 파싱해서 기기 이름 생성"""
    
    if not user_agent_string:
        return "Unknown Device"
    
    try:
        user_agent = parse(user_agent_string)
        
        # 모바일 기기
        if user_agent.is_mobile:
            device = user_agent.device.family
            os = user_agent.os.family
            browser = user_agent.browser.family
            
            if device and device != "Other":
                return f"{device} ({os})"
            else:
                return f"{browser} on {os}"
        
        # 태블릿
        elif user_agent.is_tablet:
            device = user_agent.device.family
            os = user_agent.os.family
            browser = user_agent.browser.family
            
            if device and device != "Other":
                return f"{device} ({os})"
            else:
                return f"{browser} on {os}"
        
        # 데스크톱/PC
        else:
            os = user_agent.os.family
            browser = user_agent.browser.family
            
            # Windows, macOS 등 운영체제 정보가 있는 경우
            if os and os != "Other":
                return f"{browser} on {os}"
            else:
                return f"{browser}"
                
    except Exception:
        # 파싱 실패 시 기본값
        return "Unknown Device"