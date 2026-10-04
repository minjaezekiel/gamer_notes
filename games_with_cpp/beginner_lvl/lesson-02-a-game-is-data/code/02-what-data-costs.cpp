// ===========================================================================
// 02 - What your data actually costs
// Lesson 2, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 02-what-data-costs.cpp -o 02-costs
// RUN:      ./02-costs
//
// WHAT THIS SHOWS:  C++ lets you ASK how much memory something takes. You
//                   rarely need to. Knowing the question exists is part of
//                   knowing why games are written in C++.
//
// TRY THIS:         add a field to Fighter and run it again. Then try making
//                   the name much longer and notice sizeof does NOT change -
//                   working out why is a question in the notes.
// ===========================================================================

#include <iostream>
#include <string>

struct Fighter {
    std::string name;
    int health;
    int max_health;
    int attack;
    int defence;
};

struct ParticleWithDoubles {
    double x, y;
    double speed_x, speed_y;
};

struct ParticleWithFloats {
    float x, y;
    float speed_x, speed_y;
};


int main() {
    std::cout << "How many bytes each type takes on this machine:\n\n";
    std::cout << "  char    " << sizeof(char) << "   (always 1)\n";
    std::cout << "  bool    " << sizeof(bool) << "\n";
    std::cout << "  int     " << sizeof(int) << "\n";
    std::cout << "  float   " << sizeof(float) << "\n";
    std::cout << "  double  " << sizeof(double) << "\n";
    std::cout << "  Fighter " << sizeof(Fighter) << "   (the whole bundle)\n";

    // ---- WHY THIS MATTERS ---------------------------------------------------
    const int PARTICLES = 100000;
    std::size_t with_doubles = sizeof(ParticleWithDoubles) * PARTICLES;
    std::size_t with_floats = sizeof(ParticleWithFloats) * PARTICLES;

    std::cout << "\n" << PARTICLES << " particles would need:\n";
    std::cout << "  using double: " << with_doubles / 1024 << " KB\n";
    std::cout << "  using float:  " << with_floats / 1024 << " KB\n";
    std::cout << "  the float version is " << with_doubles / with_floats
              << "x smaller.\n";
    std::cout << "\nThat is not just about running out of memory. Smaller data\n";
    std::cout << "fits in the processor's fast cache, and a game can run twice\n";
    std::cout << "as fast for that reason alone.\n";

    // ---- AN INT CAN OVERFLOW -------------------------------------------------
    int score = 2147483647;        // the largest an int can hold
    std::cout << "\nThe biggest int is " << score << ".\n";
    score = score + 1;
    std::cout << "Add one and you get " << score << ".\n";
    std::cout << "It wrapped round to the bottom. An int is 32 bits, so it\n";
    std::cout << "holds about plus or minus 2.1 billion - and past the top it\n";
    std::cout << "comes back at the bottom. Real games have shipped with this.\n";

    // Note: we worked out the overflow using a value we already know, rather
    // than letting the compiler compute it. Signed overflow is actually
    // "undefined behaviour" in C++, which means the compiler is allowed to do
    // anything at all with it - another reason to be careful with big numbers.

    return 0;
}
