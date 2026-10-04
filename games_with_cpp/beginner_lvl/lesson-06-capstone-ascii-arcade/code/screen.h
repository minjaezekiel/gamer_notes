// ===========================================================================
// screen.h - the screen buffer: WHAT EXISTS
//
// A HEADER holds DECLARATIONS: the names and shapes of things, so other files
// know what they may call. It is the menu, not the kitchen.
//
// Any file that wants to draw writes  #include "screen.h"  and can then call
// put() - without knowing or caring how it works.
// ===========================================================================

#pragma once
// "Only read this file once per compilation."
// Two files both including screen.h would otherwise declare everything twice,
// and the compiler would complain. Put this at the top of EVERY header.
//
// You will also see the older form - #ifndef SCREEN_H / #define SCREEN_H /
// #endif - called an include guard. It does the same job.

#include <string>

const int WIDTH = 46;
const int HEIGHT = 20;

void clear(char background);
void put(int x, int y, char c);
void put_text(int x, int y, const std::string& text);
void present(const std::string& status);
