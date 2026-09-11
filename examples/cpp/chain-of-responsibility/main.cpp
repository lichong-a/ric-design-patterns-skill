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

class Rule {
    std::function<bool(int)> accepts;
    std::unique_ptr<Rule> next;
public:
    Rule(std::function<bool(int)> f, std::unique_ptr<Rule> n = nullptr): accepts(std::move(f)), next(std::move(n)) {}
    bool handle(int value) const { return accepts(value) && (!next || next->handle(value)); }
};

int main() {
    int visits = 0;
    Rule chain{[](int n){ return n > 0; }, std::make_unique<Rule>([&](int n){ ++visits; return n < 10; })};
    check(!chain.handle(-1) && visits == 0);
    check(chain.handle(5) && visits == 1);
    check(!chain.handle(12) && visits == 2);
    std::cout << "OK chain-of-responsibility\n";
}
