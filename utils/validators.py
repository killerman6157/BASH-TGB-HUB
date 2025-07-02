import re

def is_valid_phone_number(phone: str) -> bool:
    """
    Duba ko phone number valid ne (e.g. +2348123456789)
    """
    pattern = r'^\+\d{10,15}$'
    return re.match(pattern, phone) is not None

def is_2fa_error(error: Exception) -> bool:
    """
    Duba ko exception da aka samu 2FA/password ne
    """
    text = str(error).lower()
    return "2fa" in text or "password" in text or "cloud password" in text

def mask_phone(phone: str) -> str:
    """
    Masaki lambar waya domin privacy (e.g. +234******6789)
    """
    return phone[:5] + "******" + phone[-4:]
