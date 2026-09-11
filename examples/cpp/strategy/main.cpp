#include <algorithm>
#include <functional>
#include <iostream>
#include <map>
#include <memory>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using std::string;
void check(bool value) { if (!value) throw std::runtime_error("check failed"); }
template<class F> void expect_error(F action) {
    bool failed = false;
    try { action(); } catch (const std::logic_error&) { failed = true; }
    check(failed);
}

class Pricing {
    std::function<int(int)> rule;
public:
    explicit Pricing(std::function<int(int)> r): rule(std::move(r)) {}
    void set(std::function<int(int)> r) { rule = std::move(r); }
    int quote(int base) const {
        if (base < 0) throw std::invalid_argument("base");
        return rule(base);
    }
};

int main() {
    Pricing pricing{[](int n){ return std::max(0, n - 10); }};
    check(pricing.quote(100) == 90);
    pricing.set([](int n){ return std::max(0, n - 20); });
    check(pricing.quote(100) == 80 && pricing.quote(5) == 0);
    expect_error([&]{ pricing.quote(-1); });
    std::cout << "OK strategy\n";
}
