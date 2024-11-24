import sys
import os
import time

# Terminal effects
def clear_terminal():
    """Clears the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter_effect(text, delay=0.05):
    """
    Takes text as input and outputs it with a typewriter effect.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def blinking_effect(text, duration=3, interval=0.5):
    """Displays blinking text in terminal for the input duration"""
    end_time = time.time() + duration
    while time.time() < end_time:
        clear_terminal()
        print(text)
        time.sleep(interval)
        clear_terminal()
        time.sleep(interval)
