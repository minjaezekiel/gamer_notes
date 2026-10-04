// ===========================================================================
// main.cpp - the loop, and nothing else
//
// BUILD:    make
// RUN:      ./invaders        <- from a REAL TERMINAL
// CLEAN:    make clean
//
// Look at how short this file is. All it does is run the loop and hand work to
// the other files. That is what splitting a program buys you: each file has
// one job, and this one's job is TIMING.
// ===========================================================================

#include "game.h"
#include "screen.h"
#include "terminal.h"

#include <chrono>
#include <iostream>
#include <thread>

using Clock = std::chrono::steady_clock;
// steady_clock, NOT system_clock: the system clock can jump when the machine
// syncs with a time server or daylight saving starts.

// ---- THE FIXED TIMESTEP ----------------------------------------------------
// The physics ALWAYS advances by exactly this much, whatever the frame rate.
static const double STEP = 1.0 / 60.0;

// Never try to catch up more than this in one frame. Without this clamp, a ten
// second stall would try to run 600 updates at once, which takes even longer,
// which makes the next gap bigger - a "spiral of death" the game never
// recovers from.
static const double MAX_CATCH_UP = 0.25;

static const auto TARGET_FRAME_TIME = std::chrono::microseconds(1000000 / 60);
static const double TIME_LIMIT = 120.0;      // so the demo ends on its own


int main() {
    start_raw_mode();
    std::cout << "\033[2J";

    auto program_start = Clock::now();
    auto last_time = Clock::now();
    double accumulator = 0.0;
    bool running = true;

    while (running) {
        auto frame_start = Clock::now();

        // ---- how much real time has passed? ----
        std::chrono::duration<double> delta = frame_start - last_time;
        last_time = frame_start;
        double frame_time = delta.count();
        if (frame_time > MAX_CATCH_UP) {
            frame_time = MAX_CATCH_UP;
        }

        // ---- INPUT ----
        int key = read_key();
        if (key == 'q' || key == 'Q') {
            running = false;
        } else {
            game_handle_key(key);
        }

        // ---- UPDATE, in fixed steps ----
        accumulator += frame_time;
        while (accumulator >= STEP) {
            game_update(STEP);      // ALWAYS exactly 1/60 of a second
            accumulator -= STEP;
            // SUBTRACT, do not zero it. The leftover time is kept for next
            // frame, so the game stays exactly in step with the real world.
        }
        //
        // Because update() always gets the same dt, the steps can never get
        // big - so a fast bullet cannot jump straight THROUGH an alien. That
        // is "tunnelling", and the fixed timestep is the real cure for it.
        //
        // It also makes the game REPEATABLE: the same inputs produce the same
        // result every time, which is what makes replays and online
        // multiplayer possible at all.

        // ---- RENDER ----
        game_draw();
        present(game_status_line());

        if (std::chrono::duration<double>(frame_start - program_start).count()
                > TIME_LIMIT) {
            running = false;
        }

        // ---- wait out the rest of the frame ----
        auto elapsed = Clock::now() - frame_start;
        if (elapsed < TARGET_FRAME_TIME) {
            std::this_thread::sleep_for(TARGET_FRAME_TIME - elapsed);
        }
    }

    stop_raw_mode();        // ALWAYS. Put the terminal back.

    std::cout << "\nFinal score: " << game_score() << "\n";
    return 0;
}
