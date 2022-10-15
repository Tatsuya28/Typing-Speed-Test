import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin the test!")
    stdscr.refresh()
    stdscr.getkey()


def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()     # Don't forget to remove the '\n'


def display_text(stdscr, target, current, wpm: float = 0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM : {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        # len(current_text) / (time_elapsed / 60) gives the number of character per minute
        # we divide by 5 because we assume that 5 is the average word's number of characters
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5, 1)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # If we have finished to type the text without any mistake
        if "".join(current_text) == target_text:  # convert a list in a string
            stdscr.nodelay(False)
            stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
            break

        try:
            key = stdscr.getkey()
        except Exception:
            continue

        if key in ("KEY_ESCAPE", '\x1b'):
            stdscr.nodelay(False)
            stdscr.addstr(3, 0, "Press any key to restart. Press another time ESC to quit...")
            break
        if key in ("KEY_BACKSPACE", '\b', '\x7f'):
            if current_text:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    """

    :param stdscr: standard output screen
    :return:
    """
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        key = stdscr.getkey()
        if key in ("KEY_ESCAPE", '\x1b'):
            break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wrapper(main)
