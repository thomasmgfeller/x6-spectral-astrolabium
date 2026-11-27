// Equations and branch-and-bound implementation from the pinned prior archive.
#define equations archived_equations
#include "gleichungen.hpp"
#undef equations

void equations(const Model& model, const Fields& at, const Fields& half,
               int small, Vec& residual, Mat& jacobian) {
    archived_equations(model, at, half, small, residual, jacobian);
    if (!model.occupied) {
        // Keep the existing 11-coordinate representation with the exact constraint w21 = 0.
        // G21 is still a field equation. The density variation at 21 is absent.
        residual[3] = at.w[21];
        jacobian[3] = {};
        jacobian[3][10] = point(S);
    }
}
#include "suche.hpp"

int main(int argc, char** argv) {
    assert(argc == 6);
    const std::string type = argv[1], mode = argv[5];
    const bool before = type.front() == 'A', positive = type.back() == '+';
    assert(type == "A0" || type == "A+" || type == "B+");
    const int small = std::stoi(argv[2]), depth = std::stoi(argv[3]), budget = std::stoi(argv[4]);
    assert(small >= 0 && small <= 3 && depth >= 0 && budget > 0);
    int size;
    std::cin >> size;
    std::vector<std::pair<int,int>> order(size);
    for (auto& [a,b] : order) std::cin >> a >> b;
    Fields base;
    base.y.fill({-5*S, 2*S});
    base.w.fill({0,S});
    for (int j : {15,17,20}) base.w[j] = point(0);
    if (!positive) base.w[21] = point(0);
    for (int i = 0; i < 8; ++i) {
        int j;
        std::cin >> j;
        std::cin >> base.y[j].l >> base.y[j].h >> base.w[j].l >> base.w[j].h;
    }
    Box window;
    std::cin >> window.l >> window.h;
    assert(base.y[0].l == -5*S && base.y[7].h == 2*S);
    assert(window.l > base.y[0].h && window.h < base.y[7].l);
    base.y[19] = base.y[20] = window;
    Row row;
    for (int& mask : row) std::cin >> mask;
    Model model(order, row, before, positive);
    // The initial clock box covers every free event either by chronology to 0 and 7
    // or by the measurement at 19 and the genuine relation 21 < 19.
    for (int j : FREE) {
        assert(model.past[j] & 1);
        if (!(model.future[j] & (1 << 7))) {
            assert(before && (j == 19 || (j == 21 && (model.future[21] & (1 << 19)))));
        }
    }
    for (int j = 15; j <= 21; ++j) {
        for (auto e : model.inc[j]) assert(e.j >= 15 || e.j <= 3);
        for (auto e : model.out[j]) assert(e.j >= 15 || (e.j >= 7 && e.j <= 10));
    }
    if (mode == "order") {
        for (int i = 0; i < N; ++i)
            for (int j = 0; j < N; ++j)
                if (model.future[i] & (1 << j)) {
                    int c = 0;
                    for (auto e : model.out[i]) if (e.j == j) c = e.c;
                    std::cout << i << ' ' << j << ' ' << c << '\n';
                }
        return 0;
    }
    Test test{model, base};
    for (int p = 0; p < 2; ++p)
        test.f.w[pos[p]] = (small & (1 << p)) ? Box{0,10} : Box{10,S};
    if (mode == "algebra" || mode == "control") {
        for (int i = 0; i < K; ++i) {
            Box value;
            std::cin >> value.l >> value.h;
            axis(test.f, i) = value;
        }
    }
    if (mode == "algebra") {
        Vec residual{};
        Mat jacobian{};
        equations(model, test.f, test.f, small, residual, jacobian);
        for (int i = 0; i < K; ++i) {
            std::cout << residual[i].l << ' ' << residual[i].h;
            for (Box v : jacobian[i]) std::cout << ' ' << v.l << ' ' << v.h;
            std::cout << '\n';
        }
    } else {
        assert(mode == "tree" || mode == "control");
        Results s;
        search(test, small, s, 0, depth, budget);
        assert(s.nodes == 2*(s.closed+s.open)-1);
        std::cout << s.nodes << ' ' << s.closed << ' ' << s.open << ' ' << s.depth << '\n';
    }
    assert(std::cin && std::cout);
}
