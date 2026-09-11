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

struct Toggle {
    std::function<void(bool)> changed;
    void set(bool enabled) { if (changed) changed(enabled); }
};
struct SubmitButton { bool enabled = false; };
class Dialog {
public:
    Toggle toggle; SubmitButton submit;
    Dialog() { toggle.changed = [this](bool enabled){ submit.enabled = enabled; }; }
    Dialog(const Dialog&) = delete; Dialog& operator=(const Dialog&) = delete;
    Dialog(Dialog&&) = delete; Dialog& operator=(Dialog&&) = delete;
};

int main() {
    Dialog dialog;
    check(!dialog.submit.enabled);
    dialog.toggle.set(true); check(dialog.submit.enabled);
    dialog.toggle.set(false); check(!dialog.submit.enabled);
    std::cout << "OK mediator\n";
}
