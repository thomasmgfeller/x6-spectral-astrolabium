// The verifier extracts this computational core from the SHA-256 pinned parent.
#include "zweigkern.hpp"

int main(int argc, char** argv) {
    assert(argc == 4 || argc == 5);
    int depth = std::stoi(argv[1]);
    int budget = std::stoi(argv[2]);
    int sector = std::stoi(argv[3]);
    assert(depth >= 0 && budget > 0 && sector >= 0 && sector <= 3);

    int count;
    std::cin >> count;
    std::vector<std::pair<int, int>> order(count);
    for (auto& [a, b] : order) std::cin >> a >> b;
    Fields base;
    base.y.fill({-5*S, 2*S});
    base.w.fill({0, S});
    for (int j : {15, 17, 20}) base.w[j] = point(0);
    for (int i = 0; i < 8; ++i) {
        int j;
        std::cin >> j;
        std::cin >> base.y[j].l >> base.y[j].h >> base.w[j].l >> base.w[j].h;
    }
    for (int expected : DUST) {
        int j;
        std::cin >> j;
        assert(j == expected);
        std::cin >> base.y[j].l >> base.y[j].h;
    }
    Box window;
    std::cin >> window.l >> window.h;
    assert(window.l > base.y[0].h && window.h < base.y[7].l);
    base.y[19] = base.y[20] = window;
    std::cin >> count;
    assert(count == 1);
    Row row;
    for (int& mask : row) std::cin >> mask;
    Model model(order, row, false, true);
    Test test{model, base};
    for (int j = 15; j <= 21; ++j) {
        assert(model.past[j] & 1);
        if (!(model.future[j] & (1 << 7)) && j != 19 && j != 20) {
            assert(j == 21 && (model.future[21] & (1 << 8)));
            test.f.y[21] = {base.y[0].l, base.y[8].h};
        }
        for (auto e : model.inc[j])
            assert(e.j >= 15 || e.j <= 3 ||
                   std::find(std::begin(DUST), std::end(DUST), e.j) != std::end(DUST));
        for (auto e : model.out[j])
            assert(e.j >= 15 || (e.j >= 7 && e.j <= 10));
    }
    for (int i = 0; i < 2; ++i)
        test.f.w[pos[i]] = sector & (1 << i) ? Box{0, 10} : Box{10, S};
    if (argc == 5) {
        for (int i = 0; i < K; ++i) {
            Box b;
            std::cin >> b.l >> b.h;
            axis(test.f, i) = b;
        }
        if (std::string(argv[4]) == "algebra") {
            Vec values{};
            Mat jac{};
            equations(model, test.f, test.f, sector, values, jac);
            for (int i = 0; i < K; ++i) {
                std::cout << values[i].l << ' ' << values[i].h;
                for (Box b : jac[i]) std::cout << ' ' << b.l << ' ' << b.h;
                std::cout << '\n';
            }
            assert(std::cin && std::cout);
            return 0;
        }
        assert(std::string(argv[4]) == "control");
    }
    Results stats;
    search(test, sector, stats, 0, depth, budget);
    assert(stats.nodes == 2*(stats.closed + stats.open) - 1);
    std::cout << row[1] << ' ' << sector << ' ' << stats.nodes << ' '
              << stats.closed << ' ' << stats.open << ' ' << stats.depth << '\n';
    assert(std::cin && std::cout);
}
