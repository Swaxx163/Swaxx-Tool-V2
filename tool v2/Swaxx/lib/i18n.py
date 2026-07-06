"""Swaxx-Tools — SV/EN helpers."""
from .config import get_settings

def is_sv() -> bool:
    return get_settings().lang == "sv"

def t(sv: str, en: str) -> str:
    return sv if is_sv() else en

def reload_settings() -> None:
    get_settings().reload()