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

struct Counter { int value = 0; };
class AddCommand {
    Counter& counter; int delta; int before = 0;
    enum class Phase { fresh, done, undone }; Phase phase = Phase::fresh;
public:
    AddCommand(Counter& c, int d): counter(c), delta(d) {}
    void execute() {
        if (phase != Phase::fresh) throw std::logic_error("execute once");
        before = counter.value; counter.value += delta; phase = Phase::done;
    }
    void undo() {
        if (phase != Phase::done) throw std::logic_error("nothing to undo");
        counter.value = before; phase = Phase::undone;
    }
};

int main() {
    Counter counter; AddCommand command{counter, 3};
    expect_error([&]{ command.undo(); });
    command.execute(); check(counter.value == 3);
    expect_error([&]{ command.execute(); });
    command.undo(); check(counter.value == 0);
    expect_error([&]{ command.undo(); });
    std::cout << "OK command\n";
}
