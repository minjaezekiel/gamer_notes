// ===========================================================================
// 01 - Copies versus the real thing
// Lesson 2, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 01-copies-vs-references.cpp -o 01-copies
// RUN:      ./01-copies
//
// WHAT THIS SHOWS:  The single most important idea in C++, and the one that
//                   costs beginners the most time. One character - "&" -
//                   decides whether a function works on YOUR data or on a
//                   throwaway photocopy of it.
//
// THE KEY POINT:    getting it wrong produces NO ERROR AND NO WARNING. The
//                   program runs perfectly and simply does nothing.
// ===========================================================================

#include <iostream>
#include <string>

struct Fighter {
    std::string name;
    int health;
};
// Note the semicolon after the closing brace. A struct declaration is a
// statement, so it needs one. Forgetting it gives a confusing error that
// usually points at whatever comes NEXT.


// ---- BY VALUE: the function gets a PHOTOCOPY -------------------------------
void hurt_a_copy(Fighter fighter) {
    fighter.health -= 10;
    std::cout << "    inside the function, health is now "
              << fighter.health << "\n";
    // ...and when this function ends, that copy is thrown away.
}


// ---- BY REFERENCE: the function gets THE REAL ONE --------------------------
void hurt_the_real_one(Fighter& fighter) {
    //                        ^ one character. That is the whole difference.
    fighter.health -= 10;
    std::cout << "    inside the function, health is now "
              << fighter.health << "\n";
}


// ---- CONST REFERENCE: the real one, but READ-ONLY --------------------------
// Use this for anything big you only need to READ. You get the speed of a
// reference with the safety of a copy: the compiler refuses to let you change
// it. Try un-commenting the line inside and see what happens.
void describe(const Fighter& fighter) {
    // fighter.health = 999;    // <-- un-comment this: it will NOT compile
    std::cout << "    " << fighter.name << " has " << fighter.health << " hp\n";
}


int main() {
    Fighter troll;
    troll.name = "Cave troll";
    troll.health = 120;

    std::cout << "Start:            " << troll.health << "\n\n";

    std::cout << "hurt_a_copy(troll):\n";
    hurt_a_copy(troll);
    std::cout << "  after the call:  " << troll.health
              << "   <- UNCHANGED. The function hurt a photocopy.\n\n";

    std::cout << "hurt_the_real_one(troll):\n";
    hurt_the_real_one(troll);
    std::cout << "  after the call:  " << troll.health
              << "   <- CHANGED. The function had the real one.\n\n";

    std::cout << "describe(troll):\n";
    describe(troll);

    std::cout << "\n";
    std::cout << "Remember: & means THE ACTUAL ONE.\n";
    std::cout << "Without it you get a photocopy, and scribbling on a\n";
    std::cout << "photocopy leaves the original untouched - with no error\n";
    std::cout << "and no warning to tell you.\n";

    return 0;
}
