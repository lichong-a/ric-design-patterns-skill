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

class Events {
    std::map<int, std::function<void(int)>> listeners;
    int sequence = 0;
public:
    int subscribe(std::function<void(int)> fn) { int id = ++sequence; listeners.emplace(id, std::move(fn)); return id; }
    void unsubscribe(int id) { listeners.erase(id); }
    void emit(int value) {
        auto snapshot = listeners;
        for (auto& entry : snapshot) entry.second(value);
    }
};

int main() {
    Events events; std::vector<int> seen;
    auto token = events.subscribe([&](int n){ seen.push_back(n); });
    events.emit(1); events.unsubscribe(token); events.emit(2);
    check(seen == std::vector<int>{1});
    int self = 0; self = events.subscribe([&](int){ events.unsubscribe(self); });
    events.emit(3); events.emit(4);
    std::cout << "OK observer\n";
}
