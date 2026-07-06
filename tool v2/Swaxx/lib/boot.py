"""Cinematic boot sequence."""
import os, sys, time, shutil, math, random, webbrowser
import msvcrt
from . import constants as C

LOGO_RAW = r"""
   ███████╗██╗    ██╗ █████╗ ██╗  ██╗██╗  ██╗
   ██╔════╝██║    ██║██╔══██╗╚██╗██╔╝╚██╗██╔╝
   ███████╗██║ █╗ ██║███████║ ╚███╔╝  ╚███╔╝ 
   ╚════██║██║███╗██║██╔══██║ ██╔██╗  ██╔██╗ 
   ███████║╚███╔███╔╝██║  ██║██╔╝ ██╗██╔╝ ██╗
   ╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
""".strip("\n")

_RAIN_CHARS = list("01▓▒░│┤╣║╗╝┐└┴┬├─┼╚╔╩╦╠═╬┘┌ヲァィゥェォカキクケコAB3F9E#%&?$@!")

def _ansi_rgb(r,g,b): return f"\033[38;2;{r};{g};{b}m"
def _ansi_reset(): return "\033[0m"
def _ansi_goto(row,col): return f"\033[{row};{col}H"
def _ansi_hide_cursor(): return "\033[?25l"
def _ansi_show_cursor(): return "\033[?25h"
def _ansi_clear(): return "\033[2J\033[H"
def _write(s): sys.stdout.write(s); sys.stdout.flush()

def check_skip_boot():
    if msvcrt.kbhit():
        msvcrt.getch()
        return True
    return False

def _phase_vector_scan(tw, th, duration=1.8):
    pass

def _phase_vector_build(tw, th, logo_lines):
    pass

def _phase_vector_idle(tw, th, logo_lines):
    pass

def _cinematic_boot():
    """Simplified but functional boot."""
    logo_lines = LOGO_RAW.split("\n")
    tw, th = shutil.get_terminal_size((120, 35))
    _write(_ansi_hide_cursor())
    try:
        for line in logo_lines:
            print(line)
            time.sleep(0.05)
        prompt = "[ PRESS ENTER TO ACCESS THE SWAXX ]"
        print("\n" * 2 + prompt)
        input()
    except Exception:
        pass
    finally:
        _write(_ansi_show_cursor() + _ansi_clear())

def boot(skip_anim=False):
    if not skip_anim:
        _cinematic_boot()