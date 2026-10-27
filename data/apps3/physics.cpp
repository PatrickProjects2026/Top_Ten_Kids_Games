#include <iostream>
#include <string>
#include <vector>

int main(int argc, char *argv[])
{
    // We expect: physics.exe, char_x, char_state, last_key
    // That is 4 arguments total.
    if (argc < 4)
    {
        return 1; // Exit with error if Python didn't send enough data
    }

    try
    {
        double x = std::stod(argv[1]);
        int currentState = std::stoi(argv[2]);
        std::string key = argv[3];

        double speed = 7.0;
        int nextState = currentState;

        // Logic
        if (key == "SPACE")
        {
            nextState = 2; // ATTACK
        }
        else if (key == "LEFT")
        {
            x -= speed;
            nextState = 1; // WALK
        }
        else if (key == "RIGHT")
        {
            x += speed;
            nextState = 1; // WALK
        }
        else
        {
            nextState = 0; // IDLE
        }

        // Boundary safety
        if (x < 0)
            x = 0;
        if (x > 560)
            x = 560;

        // Output to Python
        std::cout << x << " " << nextState << std::endl;
    }
    catch (...)
    {
        return 1; // Exit with error if numbers are formatted badly
    }

    return 0; // Success!
}