// Simulation-only adapter: emit the oriented strict closure, little-endian bits per row.
// Coordinates are never supplied to the statistical decision. Input contains binary64 xyzt rows in t,x,y,z order.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    const int n = std::atoi(argv[1]);
    if (n < 2 || n > 100000) return 2;
    std::vector<std::array<double,4>> points(n);
    if (std::fread(points.data(), sizeof(points[0]), n, stdin) != static_cast<size_t>(n)) return 3;
    if (std::fgetc(stdin) != EOF) return 4;
    for (const auto& p : points) for (double x : p) if (!std::isfinite(x)) return 5;
    std::vector<std::uint8_t> row((n+7)/8);
    for (const auto& a : points) {
        std::fill(row.begin(), row.end(), 0);
        for (int j=0; j<n; ++j) {
            const auto& b=points[j];
            const double dt=b[0]-a[0], dx=b[1]-a[1], dy=b[2]-a[2], dz=b[3]-a[3];
            if (dt>0 && dt*dt>dx*dx+dy*dy+dz*dz)
                row[j/8] |= static_cast<std::uint8_t>(1u << (j%8));
        }
        if (std::fwrite(row.data(), 1, row.size(), stdout) != row.size()) return 6;
    }
    return std::fflush(stdout) == 0 ? 0 : 7;
}
