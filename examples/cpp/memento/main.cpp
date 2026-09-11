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

class Snapshot {
    std::shared_ptr<const int> owner; string text;
    Snapshot(std::shared_ptr<const int> o, string t): owner(std::move(o)), text(std::move(t)) {}
    friend class Editor;
};
class Editor {
    std::shared_ptr<const int> owner = std::make_shared<const int>(0);
public:
    string text;
    Editor() = default; Editor(const Editor&) = delete; Editor& operator=(const Editor&) = delete;
    Snapshot save() const { return Snapshot{owner, text}; }
    void restore(const Snapshot& s) {
        if (s.owner != owner) throw std::invalid_argument("foreign snapshot");
        text = s.text;
    }
};

int main() {
    Editor a, b; a.text = "one"; auto saved = a.save();
    a.text = "two"; a.restore(saved); check(a.text == "one");
    expect_error([&]{ b.restore(saved); });
    std::cout << "OK memento\n";
}
