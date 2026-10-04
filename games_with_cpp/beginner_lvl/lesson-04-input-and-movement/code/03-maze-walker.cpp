// ===========================================================================
// 03 - THE MAZE WALKER  (the finished lesson 4 result)
// Lesson 4, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 03-maze-walker.cpp -o 03-maze
// RUN:      ./03-maze          <- from a REAL TERMINAL
//
// CONTROLS: WASD or the arrow keys. q to quit.
//
// WHAT THIS SHOWS:  Lesson 3's screen buffer plus input that does not wait.
//                   The torch flickers and the timer counts down whether or
//                   not you press anything - which was impossible until today.
//
// CHANGE ME FIRST:  the MAZE below. Add a room. The code does not change.
//
// BREAK IT:         remove the stop_raw_mode() at the end, run it, and quit.
//                   Your terminal will stop showing what you type. The cure:
//                   type "reset" and press Enter. You will not see yourself
//                   typing. It will still work.
// ===========================================================================

#include <chrono>
#include <cmath>
#include <iostream>
#include <string>
#include <thread>

#ifdef _WIN32
  #include <conio.h>
#else
  #include <termios.h>
  #include <unistd.h>
  #include <fcntl.h>
#endif

// ---- THE MAZE, as data -----------------------------------------------------
//   #  wall     .  floor     *  key     E  exit
const char* MAZE[] = {
    "##############################",
    "#@...#........#..........#...#",
    "#.##.#.######.#.########.#.#.#",
    "#.#..........*....#....*.#.#.#",
    "#.#.####.#####.##.#.####.#.#.#",
    "#...#......#......#....#...#E#",
    "#.#########.######.###.#####.#",
    "#..........#.....*.....#.....#",
    "##############################",
};

const int WIDTH = 30;
const int HEIGHT = 9;
const int TARGET_FPS = 30;
const int TIME_LIMIT = 60;              // seconds

using Clock = std::chrono::steady_clock;

// ---- SCREEN BUFFER (lesson 3) ----------------------------------------------
char screen[WIDTH * HEIGHT];

// ---- STATE -----------------------------------------------------------------
char maze[HEIGHT][WIDTH + 1];           // a changeable copy of MAZE
int player_x = 1;
int player_y = 1;
int keys_found = 0;
int total_keys = 0;
bool running = true;
bool escaped = false;


// ===========================================================================
// NON-BLOCKING INPUT
// Reading a key without waiting is NOT standard C++, so this part differs by
// operating system. #ifdef compiles only the half that fits the machine.
// ===========================================================================
#ifndef _WIN32
static termios original_terminal;
static bool terminal_changed = false;

void start_raw_mode() {
    tcgetattr(STDIN_FILENO, &original_terminal);
    terminal_changed = true;
    termios raw = original_terminal;
    raw.c_lflag &= ~(ICANON | ECHO);    // no line buffering, no echo
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


// Our own key codes, chosen above anything a real character could be.
const int KEY_NONE = 0;
const int KEY_UP = 1000;
const int KEY_DOWN = 1001;
const int KEY_LEFT = 1002;
const int KEY_RIGHT = 1003;

int read_key() {
    int key = read_raw_key();
    if (key == 0) { return KEY_NONE; }

    // An arrow key is THREE characters: 27, then 91, then a letter code.
    // That is an ANSI escape sequence - the same family of codes you used to
    // move the cursor in lesson 3.
    if (key == 27) {
        int second = read_raw_key();
        int third = read_raw_key();
        if (second == 91) {
            if (third == 65) { return KEY_UP; }
            if (third == 66) { return KEY_DOWN; }
            if (third == 67) { return KEY_RIGHT; }
            if (third == 68) { return KEY_LEFT; }
        }
        return KEY_NONE;
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

void present(const std::string& status) {
    std::string output;
    output.reserve(WIDTH * HEIGHT + HEIGHT + status.length() + 8);
    output += "\033[H";
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) { output += screen[y * WIDTH + x]; }
        output += '\n';
    }
    output += status;
    output += "    \n";
    std::cout << output << std::flush;
}


// ===========================================================================
// THE MAZE
// ===========================================================================
char maze_at(int x, int y) {
    if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) {
        return '#';       // treat anything outside as solid wall
    }
    return maze[y][x];
}

void setup_maze() {
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            char c = MAZE[y][x];
            if (c == '@') {
                player_x = x;
                player_y = y;
                c = '.';          // the player is not part of the maze
            }
            if (c == '*') { total_keys++; }
            maze[y][x] = c;
        }
        maze[y][WIDTH] = '\0';
    }
}


// ===========================================================================
// MOVEMENT
// ===========================================================================
void try_move(int dx, int dy) {
    int new_x = player_x + dx;
    int new_y = player_y + dy;

    // CHECK FIRST, THEN MOVE.
    // Work out what is at the destination BEFORE going there. The alternative -
    // move, check, move back - works for one wall and falls apart as soon as
    // two things could stop you.
    char target = maze_at(new_x, new_y);

    if (target == '#') {
        return;                      // a wall. Do not move at all.
    }

    if (target == 'E' && keys_found < total_keys) {
        return;                      // the exit is locked until you have the keys
    }

    player_x = new_x;
    player_y = new_y;

    // What did we land on?
    if (target == '*') {
        keys_found++;
        maze[new_y][new_x] = '.';    // pick it up: remove it from the maze
    } else if (target == 'E') {
        escaped = true;
        running = false;
    }
}


// ===========================================================================
// MAIN
// ===========================================================================
int main() {
    setup_maze();
    start_raw_mode();
    std::cout << "\033[2J";

    auto program_start = Clock::now();
    const auto target_frame_time = std::chrono::microseconds(1000000 / TARGET_FPS);
    bool timed_out = false;

    while (running) {
        auto frame_start = Clock::now();
        double total_time =
            std::chrono::duration<double>(frame_start - program_start).count();

        // ---- INPUT: does NOT wait ----
        int key = read_key();
        if (key == 'q' || key == 'Q') {
            running = false;
        } else if (key == 'w' || key == 'W' || key == KEY_UP) {
            try_move(0, -1);          // up is MINUS: row 0 is the top
        } else if (key == 's' || key == 'S' || key == KEY_DOWN) {
            try_move(0, +1);
        } else if (key == 'a' || key == 'A' || key == KEY_LEFT) {
            try_move(-1, 0);
        } else if (key == 'd' || key == 'D' || key == KEY_RIGHT) {
            try_move(+1, 0);
        }

        // ---- UPDATE ----
        int time_left = TIME_LIMIT - (int)total_time;
        if (time_left <= 0) {
            timed_out = true;
            running = false;
        }

        // ---- RENDER ----
        clear(' ');
        for (int y = 0; y < HEIGHT; y++) {
            for (int x = 0; x < WIDTH; x++) {
                char c = maze[y][x];
                // The exit shows as locked until every key is collected.
                if (c == 'E' && keys_found < total_keys) { c = 'X'; }
                put(x, y, c);
            }
        }

        // A torch that flickers - and keeps flickering while you stand still,
        // which was impossible before today.
        double flicker = std::sin(total_time * 11.0) + std::sin(total_time * 7.3);
        char torch = (flicker > 0.6) ? '*' : (flicker > -0.6 ? '+' : '.');
        put(WIDTH - 2, 1, torch);

        put(player_x, player_y, '@');

        std::string status = "keys " + std::to_string(keys_found) + "/"
                           + std::to_string(total_keys)
                           + "    time " + std::to_string(time_left) + "s"
                           + "    WASD or arrows, q to quit";
        present(status);

        // ---- WAIT for the rest of the frame ----
        auto elapsed = Clock::now() - frame_start;
        if (elapsed < target_frame_time) {
            std::this_thread::sleep_for(target_frame_time - elapsed);
        }
    }

    stop_raw_mode();        // ALWAYS. Put the terminal back.

    std::cout << "\n";
    if (escaped) {
        std::cout << "You escaped with all " << total_keys << " keys.\n";
    } else if (timed_out) {
        std::cout << "Out of time. You found " << keys_found << " of "
                  << total_keys << " keys.\n";
    } else {
        std::cout << "You gave up with " << keys_found << " of "
                  << total_keys << " keys.\n";
    }
    return 0;
}
