// ===========================================================================
// screen.cpp - the screen buffer: HOW IT WORKS
//
// A SOURCE file holds DEFINITIONS: the actual code. This is the kitchen.
// ===========================================================================

#include "screen.h"
// Quotes mean "look next to this file first". Angle brackets - <iostream> -
// mean "look in the standard library". Use quotes for your own files.

#include <iostream>

// "static" at file scope means PRIVATE TO THIS FILE. No other .cpp can touch
// the buffer directly; they must go through put(), which bounds-checks.
//
// That is the point of the split: the only way to draw is the safe way.
static char buffer[WIDTH * HEIGHT];


void clear(char background) {
    for (int i = 0; i < WIDTH * HEIGHT; i++) {
        buffer[i] = background;
    }
}


void put(int x, int y, char c) {
    // ALWAYS bounds-check. C++ will not stop you writing outside an array;
    // it quietly corrupts memory and fails somewhere else, later.
    if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) {
        return;
    }
    buffer[y * WIDTH + x] = c;      // skip y rows, then x across
}


void put_text(int x, int y, const std::string& text) {
    for (int i = 0; i < (int)text.length(); i++) {
        put(x + i, y, text[i]);
    }
}


void present(const std::string& status) {
    // Build ONE string and print it ONCE. Printing character by character is
    // what makes a terminal game flicker.
    std::string output;
    output.reserve(WIDTH * HEIGHT + HEIGHT + status.length() + 8);

    output += "\033[H";             // cursor home WITHOUT clearing: less flicker
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            output += buffer[y * WIDTH + x];
        }
        output += '\n';
    }
    output += status;
    output += "      \n";

    std::cout << output << std::flush;
}
