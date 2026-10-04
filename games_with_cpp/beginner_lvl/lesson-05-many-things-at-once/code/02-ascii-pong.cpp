// ===========================================================================
// 02 - ASCII PONG  (the finished lesson 5 result)
// Lesson 5, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 02-ascii-pong.cpp -o 02-pong
// RUN:      ./02-pong          <- from a REAL TERMINAL
//
// CONTROLS: W and S (or the arrow keys) move your paddle. q quits.
//
// Everything from lessons 1 to 5:
//   L1 compiling, types, a loop     L4 non-blocking input
//   L2 structs and references       L5 std::vector, smooth movement
//   L3 screen buffer, frame timing
//
// CHANGE ME FIRST:  BALL_SPEED on line 46. Try 8.0 and 40.0.
// BREAK IT:         loop forwards through particles while erasing, and watch
//                   half of them never disappear.
// ===========================================================================

#include <chrono>
#include <cmath>
#include <iostream>
#include <random>
#include <string>
#include <thread>
#include <vector>

#ifdef _WIN32
  #include <conio.h>
#else
  #include <termios.h>
  #include <unistd.h>
  #include <fcntl.h>
#endif

// ---- CONSTANTS -------------------------------------------------------------
const int WIDTH = 46;
const int HEIGHT = 18;
const int TARGET_FPS = 30;
const int PADDLE_HEIGHT = 4;
const int WINNING_SCORE = 5;
const double PADDLE_SPEED = 18.0;    // squares per SECOND
const double OPPONENT_SPEED = 11.0;  // slower than the ball, so it is beatable
const double BALL_SPEED = 17.0;
const double STEER_STRENGTH = 11.0;
const double PARTICLE_LIFE = 0.6;
const double TIME_LIMIT = 90.0;

using Clock = std::chrono::steady_clock;

// ---- RANDOM ----------------------------------------------------------------
std::random_device seed;
std::mt19937 generator(seed());

double random_double(double low, double high) {
    std::uniform_real_distribution<double> range(low, high);
    return range(generator);
}

// ===========================================================================
// STRUCTS (lesson 2)
// ===========================================================================
struct Ball {
    double x, y;              // smooth position, so it drifts rather than jumps
    double speed_x, speed_y;  // squares per SECOND
};

struct Paddle {
    double y;                 // the TOP of the paddle
    int x;                    // the column it sits in
};

struct Particle {
    double x, y;
    double speed_x, speed_y;
    double life;              // seconds remaining
};

// ---- STATE -----------------------------------------------------------------
char screen[WIDTH * HEIGHT];
Ball ball;
Paddle player = {HEIGHT / 2.0 - PADDLE_HEIGHT / 2.0, 2};
Paddle opponent = {HEIGHT / 2.0 - PADDLE_HEIGHT / 2.0, WIDTH - 3};
std::vector<Particle> particles;      // a list that GROWS while the game runs
int player_score = 0;
int opponent_score = 0;
bool running = true;


// ===========================================================================
// NON-BLOCKING INPUT (lesson 4)
// ===========================================================================
#ifndef _WIN32
static termios original_terminal;
static bool terminal_changed = false;

void start_raw_mode() {
    tcgetattr(STDIN_FILENO, &original_terminal);
    terminal_changed = true;
    termios raw = original_terminal;
    raw.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &raw);
    fcntl(STDIN_FILENO, F_SETFL, fcntl(STDIN_FILENO, F_GETFL, 0) | O_NONBLOCK);
}
void stop_raw_mode() {
    if (terminal_changed) {
        tcsetattr(STDIN_FILENO, TCSANOW, &original_terminal);
        terminal_changed = false;
    }
}
int read_raw_key() {
    char c;
    if (read(STDIN_FILENO, &c, 1) == 1) { return (unsigned char)c; }
    return 0;
}
#else
void start_raw_mode() { }
void stop_raw_mode() { }
int read_raw_key() { return _kbhit() ? _getch() : 0; }
#endif

const int KEY_UP = 1000;
const int KEY_DOWN = 1001;

int read_key() {
    int key = read_raw_key();
    if (key == 27) {                 // an arrow key is 27, then 91, then a code
        int second = read_raw_key();
        int third = read_raw_key();
        if (second == 91) {
            if (third == 65) { return KEY_UP; }
            if (third == 66) { return KEY_DOWN; }
        }
        return 0;
    }
    return key;
}


// ===========================================================================
// DRAWING (lesson 3)
// ===========================================================================
void clear(char background) {
    for (int i = 0; i < WIDTH * HEIGHT; i++) { screen[i] = background; }
}

void put(int x, int y, char c) {
    if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) { return; }  // ALWAYS
    screen[y * WIDTH + x] = c;
}

void put_text(int x, int y, const std::string& text) {
    for (int i = 0; i < (int)text.length(); i++) { put(x + i, y, text[i]); }
}

void present(const std::string& status) {
    std::string output;
    output.reserve(WIDTH * HEIGHT + HEIGHT + status.length() + 8);
    output += "\033[H";
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) { output += screen[y * WIDTH + x]; }
        output += '\n';
    }
    output += status;
    output += "      \n";
    std::cout << output << std::flush;
}


// ===========================================================================
// PARTICLES - the reason we need a vector
// ===========================================================================
void spawn_particles(double x, double y, int count) {
    for (int i = 0; i < count; i++) {
        Particle p;
        p.x = x;
        p.y = y;

        // Pick an ANGLE, then convert to x and y. Picking random x and y
        // separately scatters into a SQUARE, with more particles heading
        // diagonally - the corners of a square are further from the centre
        // than the middles of its edges.
        double angle = random_double(0.0, 2.0 * 3.14159265358979);
        double speed = random_double(4.0, 15.0);
        p.speed_x = std::cos(angle) * speed;
        p.speed_y = std::sin(angle) * speed;

        p.life = PARTICLE_LIFE;
        particles.push_back(p);       // the vector grows to fit
    }
}

void update_particles(double dt) {
    // BACKWARDS. Erasing element i shifts everything after it down one place,
    // so a forwards loop steps over the next item and about half of the dead
    // particles survive.
    //
    // (int) matters: size() is UNSIGNED, so 0 - 1 wraps round to roughly
    // 18 quintillion and the loop never ends.
    for (int i = (int)particles.size() - 1; i >= 0; i--) {
        particles[i].x += particles[i].speed_x * dt;
        particles[i].y += particles[i].speed_y * dt;
        particles[i].life -= dt;
        if (particles[i].life <= 0.0) {
            particles.erase(particles.begin() + i);
        }
    }
}


// ===========================================================================
// GAME LOGIC
// ===========================================================================
void serve(int direction) {
    ball.x = WIDTH / 2.0;
    ball.y = HEIGHT / 2.0;
    ball.speed_x = BALL_SPEED * direction;
    ball.speed_y = random_double(-6.0, 6.0);
}

void bounce_off_paddle(const Paddle& paddle, int direction) {
    // Position first, THEN velocity - or the ball sticks and vibrates.
    ball.x = paddle.x + direction;
    ball.speed_x = std::fabs(ball.speed_x) * direction;

    // Where on the paddle did it hit? -1 top, 0 middle, +1 bottom.
    // PADDLE_HEIGHT / 2.0, NOT / 2. With whole-number division the centre
    // would be half a square out and the steering subtly wrong - one of the
    // easiest bugs in C++ to miss.
    double centre = paddle.y + PADDLE_HEIGHT / 2.0;
    double offset = (ball.y - centre) / (PADDLE_HEIGHT / 2.0);
    ball.speed_y = offset * STEER_STRENGTH;

    spawn_particles(ball.x, ball.y, 9);
}

void clamp_paddle(Paddle& paddle) {
    if (paddle.y < 1.0) { paddle.y = 1.0; }
    if (paddle.y + PADDLE_HEIGHT > HEIGHT - 1) {
        paddle.y = HEIGHT - 1 - PADDLE_HEIGHT;
    }
}

bool ball_hits(const Paddle& paddle) {
    // The ball is drawn as one square, so this is the AABB test with a
    // one-square-wide box - the four conditions collapse into two ranges.
    int bx = (int)ball.x;
    return bx == paddle.x
        && ball.y >= paddle.y - 0.5
        && ball.y <= paddle.y + PADDLE_HEIGHT - 0.5;
}

void update(double dt, int key) {
    // ---- the player's paddle ----
    if (key == 'w' || key == 'W' || key == KEY_UP) {
        player.y -= PADDLE_SPEED * dt;
    }
    if (key == 's' || key == 'S' || key == KEY_DOWN) {
        player.y += PADDLE_SPEED * dt;
    }
    clamp_paddle(player);

    // ---- the opponent ----
    // It follows the ball, but SLOWER than the ball can move, so it can be
    // beaten. A perfect opponent is a correct implementation of a bad design.
    double opponent_centre = opponent.y + PADDLE_HEIGHT / 2.0;
    if (ball.y < opponent_centre - 0.6) { opponent.y -= OPPONENT_SPEED * dt; }
    if (ball.y > opponent_centre + 0.6) { opponent.y += OPPONENT_SPEED * dt; }
    clamp_paddle(opponent);

    // ---- the ball ----
    ball.x += ball.speed_x * dt;
    ball.y += ball.speed_y * dt;

    if (ball.y < 1.0) {
        ball.y = 1.0;
        ball.speed_y = -ball.speed_y;
        spawn_particles(ball.x, ball.y, 3);
    }
    if (ball.y > HEIGHT - 2.0) {
        ball.y = HEIGHT - 2.0;
        ball.speed_y = -ball.speed_y;
        spawn_particles(ball.x, ball.y, 3);
    }

    if (ball.speed_x < 0.0 && ball_hits(player)) { bounce_off_paddle(player, +1); }
    if (ball.speed_x > 0.0 && ball_hits(opponent)) { bounce_off_paddle(opponent, -1); }

    // ---- scoring ----
    if (ball.x < 0.0) {
        opponent_score++;
        spawn_particles(1.0, ball.y, 18);
        serve(+1);
    }
    if (ball.x > WIDTH - 1.0) {
        player_score++;
        spawn_particles(WIDTH - 2.0, ball.y, 18);
        serve(-1);
    }

    if (player_score >= WINNING_SCORE || opponent_score >= WINNING_SCORE) {
        running = false;
    }
}


void draw() {
    clear(' ');

    for (int x = 0; x < WIDTH; x++) {
        put(x, 0, '#');
        put(x, HEIGHT - 1, '#');
    }
    for (int y = 1; y < HEIGHT - 1; y += 2) {
        put(WIDTH / 2, y, ':');
    }

    for (int i = 0; i < PADDLE_HEIGHT; i++) {
        put(player.x, (int)player.y + i, '|');
        put(opponent.x, (int)opponent.y + i, '|');
    }

    // Particles fade through characters as their life runs out - the same
    // "remaining / total" idea as an alpha fade in the other tracks.
    for (const Particle& p : particles) {
        double fraction = p.life / PARTICLE_LIFE;
        char c = (fraction > 0.66) ? '*' : (fraction > 0.33 ? '+' : '.');
        put((int)p.x, (int)p.y, c);
    }

    // (int) TRUNCATES - it throws the fraction away rather than rounding.
    // That is why a ball at x = 0.9 and one at x = 0.1 both draw in column 0.
    put((int)ball.x, (int)ball.y, 'o');

    put_text(WIDTH / 2 - 6, 0, " " + std::to_string(player_score)
                               + " - " + std::to_string(opponent_score) + " ");
}


int main() {
    start_raw_mode();
    std::cout << "\033[2J";
    serve(random_double(0.0, 1.0) < 0.5 ? 1 : -1);

    auto program_start = Clock::now();
    auto last_time = Clock::now();
    const auto target_frame_time = std::chrono::microseconds(1000000 / TARGET_FPS);

    while (running) {
        auto frame_start = Clock::now();

        std::chrono::duration<double> delta = frame_start - last_time;
        last_time = frame_start;
        double dt = delta.count();
        if (dt > 0.1) { dt = 1.0 / TARGET_FPS; }       // clamp

        double total_time =
            std::chrono::duration<double>(frame_start - program_start).count();
        if (total_time > TIME_LIMIT) { running = false; }

        int key = read_key();
        if (key == 'q' || key == 'Q') { running = false; }

        update(dt, key);
        update_particles(dt);
        draw();

        present("  W/S or arrows   q to quit      particles: "
                + std::to_string(particles.size()));

        auto elapsed = Clock::now() - frame_start;
        if (elapsed < target_frame_time) {
            std::this_thread::sleep_for(target_frame_time - elapsed);
        }
    }

    stop_raw_mode();        // ALWAYS

    std::cout << "\nFinal score: you " << player_score
              << ", opponent " << opponent_score << "\n";
    if (player_score >= WINNING_SCORE) { std::cout << "You win.\n"; }
    else if (opponent_score >= WINNING_SCORE) { std::cout << "The opponent wins.\n"; }
    return 0;
}
