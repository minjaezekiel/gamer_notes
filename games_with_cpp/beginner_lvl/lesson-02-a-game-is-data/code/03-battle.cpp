// ===========================================================================
// 03 - THE BATTLE  (the finished lesson 2 result)
// Lesson 2, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 03-battle.cpp -o 03-battle
// RUN:      ./03-battle
//
// WHAT THIS SHOWS:  A struct bundling related data, functions taking that
//                   struct BY REFERENCE, and a real game loop.
//
// CHANGE ME FIRST:  the numbers in make_fighter() on lines 180-181. Make the
//                   troll tougher and see whether the fight is still winnable.
//
// BREAK IT:         remove the "&" from attack(Fighter& a, Fighter& d).
//                   The program still compiles and runs - and nobody ever
//                   takes any damage. No error. No warning. That silence is
//                   the whole lesson.
// ===========================================================================

#include <algorithm>    // for std::max and std::min
#include <iostream>
#include <random>
#include <string>

// ---- CONSTANTS -------------------------------------------------------------
const int BAR_WIDTH = 16;
const int POTION_HEAL = 30;

// ---- RANDOM ----------------------------------------------------------------
std::random_device seed;
std::mt19937 generator(seed());

int random_between(int low, int high) {
    std::uniform_int_distribution<int> range(low, high);
    return range(generator);
}


// ===========================================================================
// THE STRUCT - a bundle of related variables, under one name.
//
// Use one as soon as you have two variables that always travel together.
// Without it this program would need five loose variables per fighter, and
// every function would have to take all five.
// ===========================================================================
struct Fighter {
    std::string name;
    int health;
    int max_health;
    int attack;
    int defence;
};
//  ^ the semicolon matters. A struct declaration is a statement.


// A function to build one, so nothing can be forgotten and max_health can
// never disagree with health. It also means a reader of
// make_fighter("Troll", 120, 10, 3) can see what each number means.
Fighter make_fighter(std::string name, int health, int attack, int defence) {
    Fighter f;
    f.name = name;
    f.health = health;
    f.max_health = health;      // start at full, always
    f.attack = attack;
    f.defence = defence;
    return f;
}


// ===========================================================================
// RENDER - these functions SHOW the state. They never change it.
//
// Note "const Fighter&": the real one (so nothing is copied), but READ-ONLY
// (so the compiler will refuse to let this function change anything). That is
// the usual way to pass something you only need to read.
// ===========================================================================
void draw_health_bar(const Fighter& fighter) {
    // MULTIPLY FIRST, THEN DIVIDE.
    // Writing (health / max_health) * BAR_WIDTH would give 0 every time,
    // because health / max_health is whole-number division and is 0 for
    // anything short of full health. The order genuinely matters with ints.
    int filled = (fighter.health * BAR_WIDTH) / fighter.max_health;
    filled = std::max(0, std::min(BAR_WIDTH, filled));

    std::cout << "  " << fighter.name;
    // pad the name out so the bars line up
    for (int i = (int)fighter.name.length(); i < 14; i++) {
        std::cout << " ";
    }

    std::cout << " [";
    for (int i = 0; i < BAR_WIDTH; i++) {
        std::cout << (i < filled ? '#' : '-');
    }
    std::cout << "] " << fighter.health << "/" << fighter.max_health << "\n";
}


void show_battle(const Fighter& player, const Fighter& enemy, int turn) {
    std::cout << "\n---------------------------------------------\n";
    draw_health_bar(player);
    draw_health_bar(enemy);
    std::cout << "---------------------------------------------\n";
    std::cout << "  turn " << turn << "   commands: attack, defend, potion, run\n";
}


// ===========================================================================
// UPDATE - these functions CHANGE the state.
//
// "Fighter&" - a reference. THE REAL ONE, not a copy. Remove the & and this
// function quietly modifies a throwaway photocopy instead, with no error.
// ===========================================================================
void do_attack(Fighter& attacker, Fighter& defender, bool defender_is_guarding) {
    int roll = random_between(1, 6);
    int damage = attacker.attack + roll - defender.defence;

    if (defender_is_guarding) {
        damage = damage / 2;
    }

    damage = std::max(1, damage);       // always at least a scratch

    // Clamp so health never goes below zero. A player seeing "health: -7"
    // thinks the game is broken, and the health bar would break too.
    defender.health = std::max(0, defender.health - damage);

    // "You hit" but "The troll hits" - a small thing, and sloppy output in a
    // game reads as a bug to a player even when the logic is perfect.
    std::string verb = (attacker.name == "You") ? "hit" : "hits";
    std::string target = (defender.name == "You") ? "you" : defender.name;

    std::cout << "  " << attacker.name << " " << verb << " " << target
              << " for " << damage;
    if (defender_is_guarding) {
        std::cout << " (halved by guarding)";
    }
    std::cout << ".\n";
}


void drink_potion(Fighter& fighter, int& potions) {
    if (potions <= 0) {
        std::cout << "  You have no potions left.\n";
        return;
    }
    potions--;
    int before = fighter.health;
    // Clamp the other way: never heal above the maximum.
    fighter.health = std::min(fighter.max_health, fighter.health + POTION_HEAL);
    std::cout << "  You drink a potion. Health " << before << " -> "
              << fighter.health << ".  (" << potions << " left)\n";
}


// ===========================================================================
// THE GAME LOOP
// ===========================================================================
int main() {
    // Two fighters. The SAME KIND OF THING, so a third would be one more line.
    Fighter player = make_fighter("You", 100, 12, 5);
    Fighter troll = make_fighter("Cave troll", 120, 10, 3);

    int potions = 2;
    int turn = 1;
    bool playing = true;

    std::cout << "A cave troll blocks your path.\n";

    while (playing) {
        // ---- RENDER ----
        show_battle(player, troll, turn);

        // ---- INPUT ----
        std::cout << "  > ";
        std::string command;
        if (!(std::cin >> command)) {
            break;                      // input ended
        }

        bool player_guarding = false;
        bool took_a_turn = true;

        // ---- UPDATE ----
        if (command == "attack" || command == "a") {
            do_attack(player, troll, false);
        } else if (command == "defend" || command == "d") {
            player_guarding = true;
            std::cout << "  You raise your guard.\n";
        } else if (command == "potion" || command == "p") {
            drink_potion(player, potions);
        } else if (command == "run" || command == "r") {
            std::cout << "\n  You flee. The troll keeps the cave.\n";
            playing = false;
            took_a_turn = false;
        } else {
            std::cout << "  I do not know '" << command << "'.\n";
            took_a_turn = false;
        }

        if (!playing) {
            break;
        }

        // The troll only acts if the player actually did something.
        if (took_a_turn && troll.health > 0) {
            do_attack(troll, player, player_guarding);
            turn++;
        }

        // ---- has the fight ended? ----
        if (troll.health <= 0) {
            show_battle(player, troll, turn);
            std::cout << "\n  *** The cave troll falls. You win in "
                      << turn << " turns. ***\n";
            playing = false;
        } else if (player.health <= 0) {
            show_battle(player, troll, turn);
            std::cout << "\n  *** You have fallen. The troll wins. ***\n";
            playing = false;
        }
    }

    return 0;
}
