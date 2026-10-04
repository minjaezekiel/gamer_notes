// ===========================================================================
// 01 - Vectors, and the erasing bug
// Lesson 5, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 01-vectors-and-erasing.cpp -o 01-vectors
// RUN:      ./01-vectors
//
// WHAT THIS SHOWS:  A vector growing and shrinking, and the single most common
//                   bug in all of games programming - looping forwards while
//                   removing items.
//
// You have now met this bug in JavaScript (particles), Python (fruit, bricks)
// and now C++. It is not a language problem. It is a LISTS problem.
//
// TRY THIS:  remove the (int) cast on line 96 and run it. The loop never ends,
//            because size() is UNSIGNED: 0 - 1 wraps round to about
//            18 quintillion rather than becoming -1.
// ===========================================================================

#include <iostream>
#include <string>
#include <vector>

void show(const std::string& label, const std::vector<int>& v) {
    std::cout << "  " << label;
    for (std::size_t i = label.length(); i < 34; i++) { std::cout << " "; }
    std::cout << "[";
    for (std::size_t i = 0; i < v.size(); i++) {
        if (i > 0) { std::cout << ", "; }
        std::cout << v[i];
    }
    std::cout << "]   size " << v.size() << "\n";
}


int main() {
    // ---- A VECTOR GROWS ----------------------------------------------------
    std::cout << "A std::vector is a list that grows while the program runs.\n\n";

    std::vector<int> numbers;              // starts completely empty
    show("empty", numbers);

    for (int i = 1; i <= 6; i++) {
        numbers.push_back(i * 10);         // add one to the END
    }
    show("after six push_back calls", numbers);

    std::cout << "  numbers[2] is " << numbers[2] << "\n";
    std::cout << "  numbers.size() is " << numbers.size() << "\n\n";

    // ---- THE BUG -----------------------------------------------------------
    // Remove every item that is 30 or more... the obvious way.
    std::vector<int> wrong = numbers;
    std::cout << "REMOVING 30 or more, looping FORWARDS (the bug):\n";
    show("before", wrong);

    for (std::size_t i = 0; i < wrong.size(); i++) {
        if (wrong[i] >= 30) {
            wrong.erase(wrong.begin() + i);
            // Erasing element i shifts EVERYTHING AFTER IT down one place.
            // Then i++ steps over the item that just moved into position i.
            // So roughly half of what should go, stays.
        }
    }
    show("after", wrong);
    std::cout << "  ^ 40 and 60 survived. They were skipped.\n\n";

    // ---- THE FIX: loop BACKWARDS -------------------------------------------
    std::vector<int> right = numbers;
    std::cout << "REMOVING 30 or more, looping BACKWARDS (correct):\n";
    show("before", right);

    // (int) matters. size() returns an UNSIGNED type, which cannot be
    // negative - so when it reaches 0 and you subtract 1 it wraps round to an
    // enormous number and the loop runs essentially for ever.
    // -Wall warns about comparing signed and unsigned values, which is one
    // more reason to leave it switched on.
    for (int i = (int)right.size() - 1; i >= 0; i--) {
        if (right[i] >= 30) {
            right.erase(right.begin() + i);
        }
    }
    show("after", right);
    std::cout << "  ^ correct. Going backwards, a removal can never affect an\n";
    std::cout << "    index we have not reached yet.\n\n";

    // ---- VECTORS CAN HOLD ANYTHING ----------------------------------------
    struct Particle {
        double x, y;
        double life;
    };

    std::vector<Particle> particles;
    for (int i = 0; i < 5; i++) {
        particles.push_back({(double)i, 0.0, 1.0 - i * 0.3});
    }
    std::cout << "A vector of structs: " << particles.size() << " particles, ";

    int alive = 0;
    for (const Particle& p : particles) {       // read-only loop over them all
        if (p.life > 0.0) { alive++; }
    }
    std::cout << alive << " still alive.\n";

    std::cout << "\nNOTE: you may not erase from a vector inside a range-based\n";
    std::cout << "for loop like the one above. Doing so is undefined behaviour:\n";
    std::cout << "it may crash, may not, and may differ between machines.\n";

    return 0;
}
