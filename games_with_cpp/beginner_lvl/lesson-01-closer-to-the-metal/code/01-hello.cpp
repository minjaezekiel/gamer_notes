// ===========================================================================
// 01 - Your first C++ program
// Lesson 1, Games with C++, Beginner
//
// COMPILE:  clang++ -std=c++17 -Wall 01-hello.cpp -o 01-hello
// RUN:      ./01-hello
//           (on Windows: 01-hello.exe)
//
// TWO STEPS, EVERY TIME. Compile, then run. If you change this file and run it
// without compiling again, you run the OLD program - and then spend twenty
// minutes wondering why your change did nothing. Everybody does this once.
//
// CHANGE ME FIRST:  the message on line 30. Then compile and run again.
// THEN TRY:         delete a semicolon and read the error carefully. Notice it
//                   often points at the line AFTER the mistake - that is where
//                   the compiler first NOTICED something was wrong.
// ===========================================================================

#include <iostream>
// "#include" means "paste in that other file, before compiling". The # makes it
// a PREPROCESSOR directive - it happens before the compiler proper even starts.
// <iostream> is the standard library's input and output code.

int main() {
    // Every C++ program starts at main(). Always. The "int" says main hands
    // back a whole number when it finishes.

    std::cout << "Hello! This program was compiled before you ran it.\n";
    //  ^        ^                                                   ^
    //  |        |                                                   a new line
    //  |        "<<" sends the thing on the right into the stream on the left
    //  "std::" means it lives in the standard library's namespace

    std::cout << "A frame at 60 fps lasts " << 1000.0 / 60.0 << " milliseconds.\n";
    // Note 1000.0 and 60.0 - the decimal points matter. With 1000 / 60 you
    // would get 16, because when BOTH sides are whole numbers C++ does
    // whole-number division and throws the fraction away.

    std::cout << "1000 / 60 as whole numbers is " << 1000 / 60 << " - the .67 is gone.\n";

    return 0;
    // 0 means "I finished with no problem". Anything else means something went
    // wrong, and other programs can check this number.
}
