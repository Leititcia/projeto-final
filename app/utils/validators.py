import re

def validate_phone(phone: str) -> bool:
    """
    Valida um número de telefone brasileiro.
    """
    if not phone:
        return True
        
    phone = re.sub(r'\D', '', phone)
    
    if len(phone) not in [10, 11]:
        return False
        
    return True

def format_phone(phone: str) -> str:

    if not phone:
        return ""

    phone = re.sub(r'\D', '', phone)
        
    if len(phone) == 11:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    return phone 