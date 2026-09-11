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

class Bag {
    std::vector<int> values;
public:
    explicit Bag(std::vector<int> v): values(std::move(v)) {}
    auto begin() const { return values.cbegin(); }
    auto end() const { return values.cend(); }
};

int main() {
    Bag bag{{1, 2, 3}};
    auto a = bag.begin(), b = bag.begin();
    check(*a++ == 1 && *a == 2 && *b == 1);
    int sum = 0; for (int v : bag) sum += v;
    check(sum == 6);
    Bag empty{{}}; check(empty.begin() == empty.end());
    std::cout << "OK iterator\n";
}
