// ===========================================================================
// 03 - THE ANIMATED DUNGEON  (the finished lesson 3 result)
// Lesson 3, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 03-animated-dungeon.cpp -o 03-dungeon
// RUN:      ./03-dungeon
//
// WHAT THIS SHOWS:  A screen buffer, a real frame timer, and animation driven
//                   by TIME rather than by frame count - so it runs at the
//                   same speed on any machine.
//
// CHANGE ME FIRST:  TARGET_FPS on line 34. Try 5 (a slideshow) and 120.
//                   Notice the animation runs at the SAME real-world speed
//                   either way, because it is driven by elapsed seconds.
//
// BREAK IT:         change "sin(total_time * 2.0)" to "sin(frame * 2.0)" and
//                   then change TARGET_FPS. The water now ripples at a
//                   different speed on a different frame rate - the same bug
//                   the web and Python tracks met as "delta time".
// ===========================================================================

#include <chrono>
#include <cmath>
#include <iostream>
#include <string>
#include <thread>

// ---- THE DUNGEON, as data --------------------------------------------------
// Edit this and the drawing code does not change at all.
const char* DUNGEON[] = {
    "################################",
    "#......................#.......#",
    "#..~~~~................#...*...#",
    "#..~~~~................#.......#",
    "#......................#########",
    "#..............................#",
    "################################",
};

const int WIDTH = 32;
const int HEIGHT = 7;
const int TARGET_FPS = 30;

using Clock = std::chrono::steady_clock;
// steady_clock, NOT system_clock. The system clock can JUMP - if the machine
// syncs with a time server, or daylight saving starts, or someone changes the
// clock. steady_clock only ever moves forward at a steady rate, which is what
// you need for measuring how long something took.

// ---- THE SCREEN BUFFER -----------------------------------------------------
char screen[WIDTH * HEIGHT];


void clear(char background) {
    for (int i = 0; i < WIDTH * HEIGHT; i++) {
        screen[i] = background;
    }
}


void put(int x, int y, char c) {
    if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) {
        return;                      // ALWAYS bounds-check
    }
    screen[y * WIDTH + x] = c;       // skip y rows, then x across
}


void present(const std::string& status) {
    std::string output;
    output.reserve(WIDTH * HEIGHT + HEIGHT + status.length() + 8);

    output += "\033[H";              // cursor home, WITHOUT clearing
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            output += screen[y * WIDTH + x];
        }
        output += '\n';
    }
    output += status;
    output += "   \n";               // trailing spaces wipe the old status

    std::cout << output << std::flush;
}


// ---- DRAW ------------------------------------------------------------------
void draw_dungeon() {
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            put(x, y, DUNGEON[y][x]);
        }
    }
}


void draw_water(double total_time) {
    // sin() slides smoothly between -1 and +1, over and over, forever.
    //
    //    sin(time * SPEED) * SIZE
    //
    // Multiply the INPUT to change how fast it wobbles.
    // Multiply the OUTPUT to change how far it wobbles.
    //
    // That one recipe is behind almost every gentle repeating motion in games:
    // bobbing items, breathing lights, swaying grass, floating platforms. Learn
    // the shape of it long before you understand the trigonometry.
    for (int y = 2; y <= 3; y++) {
        for (int x = 3; x <= 6; x++) {
            double wave = std::sin(total_time * 2.0 + x * 0.8 + y * 1.3);
            put(x, y, wave > 0.0 ? '~' : '-');
        }
    }
}


void draw_torch(double total_time) {
    // A torch that flickers irregularly, by adding two waves of different
    // speeds so the pattern does not obviously repeat.
    double flicker = std::sin(total_time * 11.0) + std::sin(total_time * 7.3);
    char c = (flicker > 0.6) ? '*' : (flicker > -0.6 ? '+' : '.');
    put(27, 2, c);
}


void draw_bat(double total_time) {
    // The bat flies back and forth across the room. Driven by TIME, so it
    // crosses in the same number of real seconds whatever the frame rate.
    double sweep = std::sin(total_time * 0.9);              // -1 .. +1
    int x = 12 + (int)(sweep * 8.0);                        // 4 .. 20
    int y = 2 + (int)(std::sin(total_time * 2.7) * 1.4);    // a little bob

    // Wings alternate, so it looks like it is flapping.
    bool wings_up = std::sin(total_time * 14.0) > 0.0;
    put(x, y, wings_up ? 'v' : 'w');
}


int main() {
    std::cout << "\033[2J";                 // clear the terminal once

    auto program_start = Clock::now();
    auto last_time = Clock::now();
    int frame = 0;
    // Start the reading at the target rather than 0. On the very first frame
    // almost no time has passed, so 1/dt is a meaningless enormous number -
    // and a nonsense value on screen looks like a bug even when it is not.
    double measured_fps = TARGET_FPS;

    const auto target_frame_time =
        std::chrono::microseconds(1000000 / TARGET_FPS);

    // Run for about 12 seconds, so the program ends on its own.
    while (std::chrono::duration<double>(Clock::now() - program_start).count() < 12.0) {
        auto frame_start = Clock::now();

        // ---- DELTA TIME ----
        std::chrono::duration<double> delta = frame_start - last_time;
        last_time = frame_start;
        double dt = delta.count();          // seconds, as a decimal
        if (dt > 0.1) {
            dt = 1.0 / TARGET_FPS;          // clamp, as in every other track
        }
        // Skip the first frame's measurement entirely: there is no previous
        // frame to measure against.
        if (frame > 0 && dt > 0.0) {
            measured_fps = measured_fps * 0.9 + (1.0 / dt) * 0.1;
        }

        double total_time =
            std::chrono::duration<double>(frame_start - program_start).count();

        // ---- 1. CLEAR ----
        clear(' ');

        // ---- 2. DRAW ----
        draw_dungeon();
        draw_water(total_time);
        draw_torch(total_time);
        draw_bat(total_time);

        // ---- 3. SHOW ----
        std::string status = "frame " + std::to_string(frame)
                           + "    " + std::to_string((int)(measured_fps + 0.5)) + " fps"
                           + "    t = " + std::to_string((int)total_time) + "s";
        present(status);

        frame++;

        // ---- 4. WAIT for the rest of the frame's budget ----
        // Note the time, do the work, see how long it took, sleep for whatever
        // is LEFT. If the work took longer than the budget, we skip the sleep
        // and the game simply runs slower - see the notes.
        auto work_done = Clock::now();
        auto elapsed = work_done - frame_start;
        if (elapsed < target_frame_time) {
            std::this_thread::sleep_for(target_frame_time - elapsed);
        }
    }

    std::cout << "\nThe animation was driven by TIME, not by frame count.\n";
    std::cout << "Change TARGET_FPS and the bat still crosses the room in the\n";
    std::cout << "same number of real seconds.\n";
    return 0;
}
