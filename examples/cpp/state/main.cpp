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

struct GateState { virtual ~GateState() = default; virtual bool open() const = 0; virtual bool coin() const = 0; virtual bool enter() const = 0; };
struct Locked final : GateState { bool open() const override { return false; } bool coin() const override { return true; } bool enter() const override { return false; } };
struct Unlocked final : GateState { bool open() const override { return true; } bool coin() const override { return true; } bool enter() const override { return false; } };
class Gate {
    std::unique_ptr<GateState> state = std::make_unique<Locked>();
    void replace(bool value) {
        if (value) state = std::make_unique<Unlocked>(); else state = std::make_unique<Locked>();
    }
public:
    bool is_open() const { return state->open(); }
    void coin() { bool next = state->coin(); replace(next); }
    void enter() { bool next = state->enter(); replace(next); }
};

int main() {
    Gate gate; check(!gate.is_open());
    gate.enter(); check(!gate.is_open());
    gate.coin(); check(gate.is_open());
    gate.coin(); check(gate.is_open());
    gate.enter(); check(!gate.is_open());
    std::cout << "OK state\n";
}
