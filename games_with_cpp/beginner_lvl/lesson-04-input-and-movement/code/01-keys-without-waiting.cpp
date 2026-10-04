// ===========================================================================
// 01 - Reading keys WITHOUT waiting
// Lesson 4, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 01-keys-without-waiting.cpp -o 01-keys
// RUN:      ./01-keys          <- from a REAL TERMINAL, not an IDE console
//
// WHAT THIS SHOWS:  The loop runs 20 times a second whether or not you press
//                   anything. The frame counter keeps going while you do
//                   nothing - which is the entire point.
//
// TRY THIS:         press an ARROW key and watch three numbers appear at once.
//                   Arrow keys send 27, then 91, then a letter code.
//
// IMPORTANT:        press q to quit PROPERLY. If you kill it with Ctrl-C the
//                   terminal is left in raw mode - type "reset" and press
//                   Enter. You will not see yourself typing. It will work.
// ===========================================================================

#include <chrono>
#include <iostream>
#include <thread>

// ---- The one place in this course where the code differs by platform -------
// Reading a key without waiting is NOT part of standard C++. The language says
// nothing about terminals, so you use whatever the operating system provides.
//
// #ifdef is a preprocessor instruction, like #include: "only compile this part
// if that name is defined". _WIN32 is defined automatically by Windows
// compilers, so each machine compiles only the half that works for it.
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
    tcgetattr(STDIN_FILENO, &original_terminal);   // REMEMBER the settings
    terminal_changed = true;

    termios raw = original_terminal;
    // Switch off two things the terminal does by default:
    //   ICANON - line buffering: it collects a whole line and waits for Enter
    //   ECHO   - printing what you type
    // A game wants each key the instant it is pressed, and does not want a "w"
    // appearing on screen when you walk left.
    //
    // ~(ICANON | ECHO) means "everything EXCEPT those two", and &= keeps only
    // what is in both. You do not need to understand bit operations today -
    // this line means "switch those two settings off".
    raw.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &raw);

    // Make read() return immediately when there is nothing, instead of waiting.
    fcntl(STDIN_FILENO, F_SETFL, fcntl(STDIN_FILENO, F_GETFL, 0) | O_NONBLOCK);
}

void stop_raw_mode() {
    // NOT OPTIONAL. The terminal belongs to the whole system, not to your
    // program. Exit without putting the settings back and the user is left
    // typing into a terminal that shows them nothing.
    if (terminal_changed) {
        tcsetattr(STDIN_FILENO, TCSANOW, &original_terminal);
        terminal_changed = false;
    }
}

int read_key() {
    char c;
    if (read(STDIN_FILENO, &c, 1) == 1) {
        return (unsigned char)c;
    }
    return 0;          // nothing pressed. Carry on anyway.
}

#else   // ---- Windows ----
void start_raw_mode() { /* conio needs no setup */ }
void stop_raw_mode() { }
int read_key() {
    return _kbhit() ? _getch() : 0;    // _kbhit asks "is a key waiting?"
}
#endif


int main() {
    start_raw_mode();

    std::cout << "The loop runs 20 times a second whether you press anything\n";
    std::cout << "or not. Press keys. Press q to quit PROPERLY.\n\n";

    int frame = 0;
    bool running = true;

    while (running && frame < 400) {
        int key = read_key();

        if (key != 0) {
            std::cout << "frame " << frame << ":  key code " << key;
            if (key >= 32 && key < 127) {
                std::cout << "  ('" << (char)key << "')";
            }
            if (key == 27) {
                std::cout << "   <- escape. An arrow key sends 27, 91, then a letter.";
            }
            std::cout << "\n" << std::flush;

            if (key == 'q') {
                running = false;
            }
        }

        // A heartbeat, so you can see the loop running while you do nothing.
        if (frame % 20 == 0) {
            std::cout << "  ...still running, frame " << frame
                      << " (nothing pressed)\n" << std::flush;
        }

        frame++;
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }

    stop_raw_mode();        // ALWAYS
    std::cout << "\nTerminal restored. Try leaving this line out once - and\n";
    std::cout << "remember the cure is to type 'reset' and press Enter.\n";
    return 0;
}
