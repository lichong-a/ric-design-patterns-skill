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

class Settings {
    Settings() = default;
public:
    Settings(const Settings&) = delete;
    Settings& operator=(const Settings&) = delete;
    static const Settings& instance() { static const Settings value; return value; }
    string mode() const { return "demo"; }
};

int main() {
    check(&Settings::instance() == &Settings::instance());
    check(Settings::instance().mode() == "demo");
    std::cout << "OK singleton\n";
}
