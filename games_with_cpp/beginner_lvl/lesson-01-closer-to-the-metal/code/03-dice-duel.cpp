// ===========================================================================
// 03 - DICE DUEL  (the finished lesson 1 result)
// Lesson 1, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 03-dice-duel.cpp -o 03-dice-duel
// RUN:      ./03-dice-duel
//
// WHAT THIS SHOWS:  A complete game with a real game loop, in C++, with no
//                   graphics at all. Same three jobs as every other track:
//                   input, update, render.
//
// CHANGE ME FIRST:  ROUNDS_TO_WIN on line 28. Try 1, then 10.
// THEN TRY:         the "statistics" command, which rolls 100,000 dice and
//                   counts them. Are they even? That is stretch goal 3.
// ===========================================================================

#include <iostream>
#include <random>
#include <string>
#include <vector>

// CAPITALS by convention means "this never changes while the game runs", so a
// reader knows not to go looking for where it gets modified.
// "const" makes the compiler ENFORCE that - try changing one below and see.
const int DICE_SIDES = 6;
const int ROUNDS_TO_WIN = 3;

// ---- RANDOM NUMBERS --------------------------------------------------------
// One generator for the whole program, seeded once from the operating system.
//   random_device  - gets a genuinely unpredictable starting number
//   mt19937        - the generator itself (the Mersenne Twister algorithm)
//   uniform_int_distribution - maps its output onto 1..6 FAIRLY
//
// You will see older code using "rand() % 6 + 1". It works, and it is slightly
// biased, because 6 does not divide evenly into the generator's range. For
// dice nobody notices. For loot drops in a game people play for a thousand
// hours, they do.
std::random_device seed;
std::mt19937 generator(seed());
std::uniform_int_distribution<int> die(1, DICE_SIDES);

// ---- STATE -----------------------------------------------------------------
// Everything the game remembers between rounds.
int player_score = 0;
int goblin_score = 0;
int rounds_played = 0;
bool playing = true;


int roll_two_dice(int& first, int& second) {
    // "int&" means a REFERENCE: the function writes straight into the caller's
    // variables rather than into copies. That is how a function can hand back
    // more than one value. You will meet references properly at intermediate
    // level - for now, read "&" as "the real one, not a copy".
    first = die(generator);
    second = die(generator);
    return first + second;
}


// ---- RENDER: shows the state, changes nothing ------------------------------
void show_score() {
    std::cout << "\n";
    std::cout << "===========================================\n";
    std::cout << " DICE DUEL        first to " << ROUNDS_TO_WIN << " wins\n";
    std::cout << " you " << player_score << "  -  " << goblin_score << " goblin";
    std::cout << "        (round " << rounds_played + 1 << ")\n";
    std::cout << "===========================================\n";
}


void show_help() {
    std::cout << "\nCommands:\n";
    std::cout << "  roll    play a round\n";
    std::cout << "  stats   roll 100000 dice and count them\n";
    std::cout << "  help    this list\n";
    std::cout << "  quit    give up\n";
}


// ---- UPDATE: changes the state ---------------------------------------------
void play_round() {
    int a = 0, b = 0, c = 0, d = 0;
    int you = roll_two_dice(a, b);
    int them = roll_two_dice(c, d);

    std::cout << "\n  You rolled    " << a << " and " << b << "  =  " << you << "\n";
    std::cout << "  Goblin rolled " << c << " and " << d << "  =  " << them << "\n";

    if (you > them) {
        player_score++;
        std::cout << "  You win the round!\n";
    } else if (them > you) {
        goblin_score++;
        std::cout << "  The goblin wins the round.\n";
    } else {
        std::cout << "  A draw. Nobody scores.\n";
    }

    rounds_played++;

    if (player_score >= ROUNDS_TO_WIN) {
        std::cout << "\n  *** YOU WIN, " << player_score << " to " << goblin_score
                  << ", in " << rounds_played << " rounds. ***\n";
        playing = false;
    } else if (goblin_score >= ROUNDS_TO_WIN) {
        std::cout << "\n  *** The goblin wins, " << goblin_score << " to "
                  << player_score << ". ***\n";
        playing = false;
    }
}


void show_statistics() {
    const int TRIALS = 100000;

    // A vector is a list that knows its own length. We make 7 slots so we can
    // use counts[1] to counts[6] and ignore counts[0] - which is a little
    // wasteful and a lot more readable than subtracting 1 everywhere.
    std::vector<int> counts(DICE_SIDES + 1, 0);

    for (int i = 0; i < TRIALS; i++) {
        counts[die(generator)]++;
    }

    std::cout << "\n  " << TRIALS << " rolls:\n";
    for (int face = 1; face <= DICE_SIDES; face++) {
        double percent = 100.0 * counts[face] / TRIALS;
        //                ^^^^^ 100.0 not 100, or whole-number division makes
        //                      every percentage come out as 0.
        std::cout << "    " << face << ": " << counts[face]
                  << "   (" << percent << "%)\n";
    }
    std::cout << "  Each face should be close to " << 100.0 / DICE_SIDES << "%.\n";
}


// ---- THE GAME LOOP ---------------------------------------------------------
int main() {
    std::cout << "DICE DUEL\n";
    show_help();

    while (playing) {
        // ---- RENDER ----
        show_score();

        // ---- INPUT ----
        // Note that the program STOPS here and waits. A real-time game cannot
        // do this, because the world has to keep moving while the player
        // thinks. That is lesson 4.
        std::cout << "> ";
        std::string command;
        if (!(std::cin >> command)) {
            break;      // input ended (Ctrl-D, or piped input ran out)
        }

        // ---- UPDATE ----
        if (command == "roll" || command == "r") {
            play_round();
        } else if (command == "stats") {
            show_statistics();
        } else if (command == "help") {
            show_help();
        } else if (command == "quit" || command == "q") {
            std::cout << "\nYou flee the goblin.\n";
            playing = false;
        } else {
            std::cout << "I do not know '" << command << "'. Try 'help'.\n";
        }
    }

    std::cout << "\nFinal score: you " << player_score
              << ", goblin " << goblin_score << "\n";
    return 0;
}
