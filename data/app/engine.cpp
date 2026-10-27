#include <iostream>
#include <cstdlib>

int main(int argc, char *argv[])
{
    if (argc > 1)
    {
        int val = std::atoi(argv[1]);
        // C++ performs the final calculation
        std::cout << val * 2;
    }
    return 0;
}