// ===========================================================================
// terminal.cpp - non-blocking keyboard input: HOW IT WORKS
//
// Reading a key without waiting is NOT part of standard C++ - the language
// says nothing about terminals. So this file is the one place that has to
// care which operating system it is on, and #ifdef picks the right half.
//
// Every other file just calls read_key().
// ===========================================================================

#include "terminal.h"

#ifdef _WIN32
  #include <conio.h>
#else
  #include <termios.h>
  #include <unistd.h>
  #include <fcntl.h>
#endif


#ifndef _WIN32

static termios original_terminal;
static bool terminal_changed = false;

void start_raw_mode() {
    tcgetattr(STDIN_FILENO, &original_terminal);    // REMEMBER the settings
    terminal_changed = true;

    termios raw = original_terminal;
    // ICANON - line buffering (collects a line and waits for Enter)
    // ECHO   - printing what you type
    raw.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &raw);

    // Make read() return immediately instead of waiting.
    fcntl(STDIN_FILENO, F_SETFL, fcntl(STDIN_FILENO, F_GETFL, 0) | O_NONBLOCK);
}

void stop_raw_mode() {
    // NOT OPTIONAL. The terminal belongs to the whole system. Leave without
    // restoring it and the user types into a terminal that shows them nothing.
    // (The cure, if that happens: type "reset" and press Enter, blind.)
    if (terminal_changed) {
        tcsetattr(STDIN_FILENO, TCSANOW, &original_terminal);
        terminal_changed = false;
    }
}

static int read_raw_key() {
    char c;
    if (read(STDIN_FILENO, &c, 1) == 1) {
        return (unsigned char)c;
    }
    return KEY_NONE;
}

#else   // ---------------- Windows ----------------

void start_raw_mode() { }
void stop_raw_mode() { }

static int read_raw_key() {
    return _kbhit() ? _getch() : KEY_NONE;
}

#endif


int read_key() {
    int key = read_raw_key();
    if (key == KEY_NONE) {
        return KEY_NONE;
    }

    // An arrow key is THREE characters: 27, then 91, then a letter code.
    if (key == 27) {
        int second = read_raw_key();
        int third = read_raw_key();
        if (second == 91) {
            if (third == 65) { return KEY_UP; }
            if (third == 66) { return KEY_DOWN; }
            if (third == 67) { return KEY_RIGHT; }
            if (third == 68) { return KEY_LEFT; }
        }
        return KEY_NONE;
    }
    return key;
}
