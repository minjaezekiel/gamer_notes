// ===========================================================================
// game.h - the game itself: WHAT EXISTS
//
// main.cpp only needs these five functions. Everything else - the aliens, the
// bullets, the scoring - is private to game.cpp. That is deliberate: the
// header is the smallest promise that still lets main.cpp do its job.
// ===========================================================================

#pragma once

#include <string>

enum class State { Menu, Playing, GameOver };
// "enum class" rather than plain "enum": the names are scoped (State::Menu)
// and the compiler will not quietly convert them to integers. It catches
// mistakes that a plain enum would let through.

void game_start();
void game_handle_key(int key);
void game_update(double dt);        // dt is ALWAYS the same - see main.cpp
void game_draw();
State game_state();
std::string game_status_line();
int game_score();
