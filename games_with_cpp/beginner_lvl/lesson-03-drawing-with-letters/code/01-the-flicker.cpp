// ===========================================================================
// 01 - Why you need a buffer  (THE FLICKER)
// Lesson 3, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 01-the-flicker.cpp -o 01-flicker
// RUN:      ./01-flicker
//
// This file is DELIBERATELY BAD. It prints each character as it works it out,
// so you WATCH the picture being assembled instead of seeing a finished frame.
// The result flickers and scrolls horribly.
//
// Compare with 02-screen-buffer.cpp, which does the same thing properly.
//
// Press Ctrl-C to stop it.
// ===========================================================================

#include <chrono>
#include <iostream>
#include <thread>

const int WIDTH = 40;
const int HEIGHT = 12;

int main() {
    std::cout << "This will flicker. That is the point. Ctrl-C to stop.\n";
    std::this_thread::sleep_for(std::chrono::seconds(2));

    for (int frame = 0; frame < 200; frame++) {
        // Clear the whole terminal every frame - part of why it flickers.
        std::cout << "\033[2J\033[H";

        int ball_x = frame % WIDTH;

        // ---- THE PROBLEM ----
        // Printing straight to the screen, one character at a time, as we work
        // each one out. Every one of these reaches the terminal immediately, so
        // the player watches the frame being built.
        for (int y = 0; y < HEIGHT; y++) {
            for (int x = 0; x < WIDTH; x++) {
                if (y == 0 || y == HEIGHT - 1 || x == 0 || x == WIDTH - 1) {
                    std::cout << '#';
                } else if (x == ball_x && y == HEIGHT / 2) {
                    std::cout << '@';
                } else {
                    std::cout << '.';
                }
            }
            std::cout << "\n";
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(40));
    }

    std::cout << "\nNow run 02-screen-buffer to see it done properly.\n";
    return 0;
}
