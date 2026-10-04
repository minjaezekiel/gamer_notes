// ===========================================================================
// game.cpp - ASCII INVADERS: HOW IT WORKS
//
// Everything from the whole C++ beginner track:
//   L1 types, a loop        L4 input, grid movement
//   L2 structs, references  L5 std::vector, smooth movement
//   L3 the screen buffer    L6 split files
// ===========================================================================

#include "game.h"
#include "screen.h"
#include "terminal.h"

#include <algorithm>
#include <cmath>
#include <random>
#include <vector>

// ---- TUNING - all in one place, easy to find and change --------------------
static const double PLAYER_SPEED = 22.0;      // squares per SECOND
static const double BULLET_SPEED = 26.0;
static const double ALIEN_DROP = 1.0;
static const double PLAYER_SHOOT_DELAY = 0.28;
static const int STARTING_LIVES = 3;
static const int ALIEN_COLUMNS = 8;
static const int ALIEN_ROWS = 3;

// ---- STRUCTS ---------------------------------------------------------------
struct Bullet {
    double x, y;
    double speed_y;        // negative is upwards
    bool from_player;
};

struct Alien {
    double x, y;
    bool alive;
};

// ---- STATE - "static" keeps all of this private to this file ---------------
static State state = State::Menu;
static double player_x = WIDTH / 2.0;
static std::vector<Bullet> bullets;
static std::vector<Alien> aliens;
static int score = 0;
static int lives = STARTING_LIVES;
static int wave = 1;
static double alien_direction = 1.0;
static double shoot_cooldown = 0.0;
static double alien_shoot_timer = 0.0;
static bool wants_left = false;
static bool wants_right = false;

static std::random_device seed;
static std::mt19937 generator(seed());

static double random_double(double low, double high) {
    std::uniform_real_distribution<double> range(low, high);
    return range(generator);
}


// ---- helpers ---------------------------------------------------------------
static double alien_speed() {
    return 2.2 + wave * 0.7;
}

static double alien_shoot_delay() {
    // A slope AND a floor. Design the limit at the same time as the slope, or
    // the game eventually becomes impossible rather than hard.
    return std::max(0.45, 1.7 - wave * 0.16);
}

static void spawn_wave() {
    aliens.clear();
    for (int row = 0; row < ALIEN_ROWS; row++) {
        for (int col = 0; col < ALIEN_COLUMNS; col++) {
            Alien a;
            a.x = 5.0 + col * 4.5;
            a.y = 3.0 + row * 2.0;
            a.alive = true;
            aliens.push_back(a);
        }
    }
    alien_direction = 1.0;
}


void game_start() {
    score = 0;
    lives = STARTING_LIVES;
    wave = 1;
    player_x = WIDTH / 2.0;
    bullets.clear();
    shoot_cooldown = 0.0;
    alien_shoot_timer = 0.0;
    wants_left = false;
    wants_right = false;
    spawn_wave();
    state = State::Playing;
}


void game_handle_key(int key) {
    if (key == KEY_NONE) {
        return;
    }

    if (state == State::Menu || state == State::GameOver) {
        if (key == ' ') { game_start(); }
        return;
    }

    // In a terminal we get one key press at a time rather than a held-key
    // state, so each press nudges the ship for a moment. Lesson 3 of the
    // intermediate level, with raylib, gives us proper held-key input.
    if (key == 'a' || key == 'A' || key == KEY_LEFT) { wants_left = true; }
    if (key == 'd' || key == 'D' || key == KEY_RIGHT) { wants_right = true; }

    if (key == ' ' && shoot_cooldown <= 0.0) {
        Bullet b;
        b.x = player_x;
        b.y = HEIGHT - 3.0;
        b.speed_y = -BULLET_SPEED;
        b.from_player = true;
        bullets.push_back(b);
        shoot_cooldown = PLAYER_SHOOT_DELAY;
    }
}


static void update_aliens(double dt) {
    bool hit_edge = false;
    double speed = alien_speed();

    for (Alien& alien : aliens) {            // "&" - the real ones, not copies
        if (!alien.alive) { continue; }
        alien.x += alien_direction * speed * dt;
        if (alien.x < 2.0 || alien.x > WIDTH - 4.0) {
            hit_edge = true;
        }
    }

    if (hit_edge) {
        alien_direction = -alien_direction;
        for (Alien& alien : aliens) {
            if (alien.alive) { alien.y += ALIEN_DROP; }
        }
    }

    // Aliens reaching the bottom ends the game immediately.
    for (const Alien& alien : aliens) {
        if (alien.alive && alien.y >= HEIGHT - 3.0) {
            lives = 0;
            state = State::GameOver;
            return;
        }
    }

    // Aliens shoot back.
    alien_shoot_timer -= dt;
    if (alien_shoot_timer <= 0.0) {
        alien_shoot_timer = alien_shoot_delay();

        std::vector<int> living;
        for (int i = 0; i < (int)aliens.size(); i++) {
            if (aliens[i].alive) { living.push_back(i); }
        }
        if (!living.empty()) {
            // Pick an index with an INTEGER distribution, not by casting a
            // random double. uniform_real_distribution(0, n) is documented as
            // [0, n) - but it is computed in floating point, and the standard
            // permits rounding to land exactly on n. If it ever did, this
            // would index one past the end of the vector: undefined behaviour,
            // and a crash that would be impossible to reproduce on demand.
            //
            // uniform_int_distribution(0, n-1) cannot do that. Use the right
            // tool rather than one that is usually right.
            std::uniform_int_distribution<int> pick(0, (int)living.size() - 1);
            int which = living[pick(generator)];
            Bullet b;
            b.x = aliens[which].x;
            b.y = aliens[which].y + 1.0;
            b.speed_y = BULLET_SPEED * 0.45;
            b.from_player = false;
            bullets.push_back(b);
        }
    }
}


static bool close_enough(double a, double b, double tolerance) {
    return std::fabs(a - b) <= tolerance;
}


static void update_bullets(double dt) {
    // BACKWARDS, because we erase as we go. Fourth time in this course.
    // (int) matters: size() is unsigned, so 0 - 1 would wrap to an enormous
    // number and the loop would never end.
    for (int i = (int)bullets.size() - 1; i >= 0; i--) {
        bullets[i].y += bullets[i].speed_y * dt;

        bool remove = false;

        if (bullets[i].y < 1.0 || bullets[i].y > HEIGHT - 1.0) {
            remove = true;
        } else if (bullets[i].from_player) {
            for (Alien& alien : aliens) {
                if (!alien.alive) { continue; }
                if (close_enough(bullets[i].x, alien.x, 1.6)
                        && close_enough(bullets[i].y, alien.y, 0.8)) {
                    alien.alive = false;
                    score += 100;
                    remove = true;
                    break;              // one alien per bullet
                }
            }
        } else {
            if (close_enough(bullets[i].x, player_x, 1.6)
                    && bullets[i].y >= HEIGHT - 3.5) {
                lives--;
                remove = true;
                if (lives <= 0) { state = State::GameOver; }
            }
        }

        if (remove) {
            bullets.erase(bullets.begin() + i);
        }
    }
}


void game_update(double dt) {
    if (state != State::Playing) {
        return;             // ONE state check, here. Not scattered everywhere.
    }

    if (shoot_cooldown > 0.0) { shoot_cooldown -= dt; }

    if (wants_left) { player_x -= PLAYER_SPEED * dt; }
    if (wants_right) { player_x += PLAYER_SPEED * dt; }
    wants_left = false;
    wants_right = false;

    player_x = std::max(2.0, std::min(WIDTH - 3.0, player_x));   // clamp

    update_aliens(dt);
    if (state != State::Playing) { return; }
    update_bullets(dt);

    // Wave cleared?
    bool any_alive = false;
    for (const Alien& alien : aliens) {
        if (alien.alive) { any_alive = true; break; }
    }
    if (!any_alive) {
        wave++;
        score += 250;
        bullets.clear();
        spawn_wave();
    }
}


void game_draw() {
    clear(' ');

    for (int x = 0; x < WIDTH; x++) {
        put(x, 0, '#');
        put(x, HEIGHT - 1, '#');
    }
    for (int y = 0; y < HEIGHT; y++) {
        put(0, y, '#');
        put(WIDTH - 1, y, '#');
    }

    if (state == State::Menu) {
        put_text(WIDTH / 2 - 7, HEIGHT / 2 - 2, "ASCII INVADERS");
        put_text(WIDTH / 2 - 10, HEIGHT / 2, "press SPACE to play");
        put_text(WIDTH / 2 - 11, HEIGHT / 2 + 2, "A/D move   SPACE shoot");
        return;
    }

    for (const Alien& alien : aliens) {
        if (!alien.alive) { continue; }
        // (int) TRUNCATES - it does not round. The simulation is smooth even
        // though the screen is a grid.
        put_text((int)alien.x - 1, (int)alien.y, "WWW");
    }

    for (const Bullet& b : bullets) {
        put((int)b.x, (int)b.y, b.from_player ? '|' : '!');
    }

    put_text((int)player_x - 1, HEIGHT - 3, "/^\\");

    if (state == State::GameOver) {
        put_text(WIDTH / 2 - 4, HEIGHT / 2, "GAME OVER");
        put_text(WIDTH / 2 - 11, HEIGHT / 2 + 2, "SPACE to play again");
    }
}


State game_state() { return state; }
int game_score() { return score; }

std::string game_status_line() {
    if (state == State::Menu) {
        return "  SPACE to start   q to quit";
    }
    std::string hearts(std::max(0, lives), '@');
    return "  score " + std::to_string(score)
         + "   lives " + hearts
         + "   wave " + std::to_string(wave)
         + "    A/D move, SPACE shoot, q quit";
}
