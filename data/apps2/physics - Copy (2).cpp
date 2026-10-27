// Example C++ Logic update
#include <iostream>

int main(int argc, char *argv[])
{
    if (argc < 4)
        return 1;

    double y = std::stod(argv[1]);
    double v = std::stod(argv[2]);
    double floor = std::stod(argv[3]);
    double gravity = 0.75;

    v += gravity;
    y += v;

    // Simple Bounce
    if (y >= floor)
    {
        y = floor;
        v *= -0.8; // Lose some energy on bounce
    }

    std::cout << y << " " << v << std::endl;
    return 0;
}