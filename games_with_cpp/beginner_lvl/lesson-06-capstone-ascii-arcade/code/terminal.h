// ===========================================================================
// terminal.h - non-blocking keyboard input
//
// The ugliest corner of the project, hidden behind three simple functions.
// That is what a header is FOR: main.cpp does not need to know that reading a
// key involves termios on Unix and conio on Windows.
// ===========================================================================

#pragma once

// Our own key codes, chosen above anything a real character could be.
const int KEY_NONE = 0;
const int KEY_UP = 1000;
const int KEY_DOWN = 1001;
const int KEY_LEFT = 1002;
const int KEY_RIGHT = 1003;

void start_raw_mode();
void stop_raw_mode();     // ALWAYS call this before exiting
int read_key();           // returns KEY_NONE if nothing was pressed
