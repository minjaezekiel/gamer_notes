// ===========================================================================
// 02 - The screen buffer
// Lesson 3, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 02-screen-buffer.cpp -o 02-buffer
// RUN:      ./02-buffer
//
// WHAT THIS SHOWS:  Build the frame in memory, THEN show it in one go.
//                   That is DOUBLE BUFFERING, and every graphics system in the
//                   world does it - from a terminal game to a modern GPU.
//
// CHANGE ME FIRST:  the index formula on line 58. Change y*WIDTH+x to
//                   x*WIDTH+y and watch the picture fall apart.
//
// TRY THIS:         remove the bounds check in put() and call put(999, 999,'X')
//                   C++ will NOT stop you. It writes into memory it does not
//                   own. It might work, print garbage, or crash - and it may do
//                   something different each run.
// ===========================================================================

#include <chrono>
#include <iostream>
#include <string>
#include <thread>

const int WIDTH = 40;
const int HEIGHT = 12;

// ---- THE SCREEN BUFFER -----------------------------------------------------
// One long line of characters. Memory has no idea what a grid is: it is a
// single sequence of bytes, and we AGREE to read it in rows of WIDTH.
char screen[WIDTH * HEIGHT];


void clear(char background) {
    for (int i = 0; i < WIDTH * HEIGHT; i++) {
        screen[i] = background;
    }
}


void put(int x, int y, char c) {
    // ---- THE BOUNDS CHECK ----
    // ALWAYS. Python raises IndexError. JavaScript gives undefined. C++
    // quietly writes into memory belonging to something else, and the program
    // misbehaves somewhere unrelated, much later. That is one of the hardest
    // kinds of bug there is, and this one "if" prevents it.
    if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) {
        return;
    }

    // index = y * WIDTH + x
    // "skip y whole rows, then count x more across".
    screen[y * WIDTH + x] = c;
}


void put_text(int x, int y, const std::string& text) {
    for (int i = 0; i < (int)text.length(); i++) {
        put(x + i, y, text[i]);
    }
}


void present() {
    // Build ONE string, then print it ONCE. Printing character by character
    // is what made 01-the-flicker.cpp flicker.
    std::string output;
    output.reserve(WIDTH * HEIGHT + HEIGHT + 8);

    // \033[H moves the cursor to the top-left WITHOUT clearing, so the new
    // frame overwrites the old one in place. That flickers far less than
    // \033[2J, which blanks the screen first.
    output += "\033[H";

    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            output += screen[y * WIDTH + x];
        }
        output += '\n';
    }

    std::cout << output << std::flush;
}


int main() {
    std::cout << "\033[2J";          // clear once, at the start

    for (int frame = 0; frame < 300; frame++) {
        // ---- 1. CLEAR ----
        clear('.');

        // ---- 2. DRAW into the buffer ----
        for (int x = 0; x < WIDTH; x++) {
            put(x, 0, '#');
            put(x, HEIGHT - 1, '#');
        }
        for (int y = 0; y < HEIGHT; y++) {
            put(0, y, '#');
            put(WIDTH - 1, y, '#');
        }

        int ball_x = 1 + (frame % (WIDTH - 2));
        put(ball_x, HEIGHT / 2, '@');

        put_text(2, 1, "frame " + std::to_string(frame));
        put_text(2, 2, "index of @ = " + std::to_string((HEIGHT / 2) * WIDTH + ball_x));

        // Proof the bounds check works: none of these crash or corrupt anything.
        put(-5, 3, 'X');
        put(999, 3, 'X');
        put(3, -99, 'X');

        // ---- 3. SHOW it, all at once ----
        present();

        std::this_thread::sleep_for(std::chrono::milliseconds(40));
    }

    std::cout << "\nNo flicker, because nothing reached the screen until the\n";
    std::cout << "whole frame was finished.\n";
    return 0;
}
