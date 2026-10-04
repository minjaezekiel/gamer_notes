// ===========================================================================
// 02 - Reading from the player, and types
// Lesson 1, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 02-reading-input.cpp -o 02-reading-input
// RUN:      ./02-reading-input
//
// WHAT THIS SHOWS:  Declaring types, reading input, and what happens when the
//                   player types something unexpected.
//
// TRY THIS:         run it and type "banana" when it asks for a number.
//                   Then comment out the std::cin.fail() check and try again.
// ===========================================================================

#include <iostream>
#include <string>

int main() {
    // ---- TYPES ----
    // In C++ you must say what KIND of thing each variable holds. That is the
    // price you pay for the speed: the compiler needs to know how much memory
    // to set aside and what operations make sense.
    //
    // Always give a variable a starting value. An uninitialised variable in
    // C++ contains whatever junk was already in that memory - it is not zero.
    int score = 0;             // a whole number
    double accuracy = 0.0;     // a number with a decimal point
    bool playing = true;       // true or false
    char grade = 'A';          // ONE character, in single quotes
    std::string name = "";     // text, in double quotes

    std::cout << "What is your name? ";
    std::getline(std::cin, name);
    // getline reads a WHOLE LINE including spaces.
    // std::cin >> name would stop at the first space, so "Ada Lovelace" would
    // only give you "Ada".

    std::cout << "How many points did you score? ";
    std::cin >> score;

    // If the player typed something that is not a number, the read FAILS and
    // score keeps the value it already had. Always check.
    if (std::cin.fail()) {
        std::cout << "\nThat was not a number, so I will assume 0.\n";
        std::cin.clear();                 // clear the error flag
        std::cin.ignore(10000, '\n');     // throw away the bad input
        score = 0;
    }

    accuracy = score / 100.0;
    // 100.0 not 100! With "score / 100" both sides are whole numbers, so C++
    // would do whole-number division and accuracy would always be 0.

    if (score >= 90) { grade = 'A'; }
    else if (score >= 75) { grade = 'B'; }
    else if (score >= 50) { grade = 'C'; }
    else { grade = 'D'; }

    std::cout << "\n";
    std::cout << "name:     " << name << "\n";
    std::cout << "score:    " << score << "\n";
    std::cout << "accuracy: " << accuracy << "\n";
    std::cout << "grade:    " << grade << "\n";
    std::cout << "playing:  " << playing << "   <- note: true prints as 1\n";

    return 0;
}
