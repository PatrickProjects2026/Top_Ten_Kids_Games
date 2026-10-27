#include <iostream>

int main(int argc, char *argv[])
{
    if (argc < 3)
        return 1;
    float y_pos = std::stof(argv[1]);
    float y_vel = std::stof(argv[2]);
    float gravity = 0.8f;

    y_vel += gravity;
    y_pos += y_vel;

    // Bounce logic
    if (y_pos > 500)
    {
        y_pos = 500;
        y_vel *= -0.8f; // Lose energy on bounce
    }

    // Output new pos and vel for Python to read
    std::cout << y_pos << " " << y_vel;
    return 0;
}