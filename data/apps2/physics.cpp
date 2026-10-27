#include <iostream>
#include <vector>
#include <cmath>
#include <string>

int main(int argc, char *argv[])
{
    if (argc < 4)
        return 1;

    // Inputs: ball_x, ball_y, ball_vel_y
    double bx = std::stod(argv[1]);
    double by = std::stod(argv[2]);
    double bvy = std::stod(argv[3]);

    // Simple Physics: Move ball
    by += bvy;

    // Pin positions (Static for this frame)
    // We output: new_bx new_by hit_index (-1 if none)
    int hit_idx = -1;
    float pin_coords[10][2] = {
        {200, 100}, {180, 80}, {220, 80}, {160, 60}, {200, 60}, {240, 60}, {140, 40}, {180, 40}, {220, 40}, {260, 40}};

    for (int i = 0; i < 10; ++i)
    {
        double dx = bx - pin_coords[i][0];
        double dy = by - pin_coords[i][1];
        if (std::sqrt(dx * dx + dy * dy) < 15)
        {
            hit_idx = i;
            break;
        }
    }

    std::cout << bx << " " << by << " " << hit_idx << std::endl;
    return 0;
}