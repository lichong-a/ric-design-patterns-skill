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

struct Button { virtual ~Button() = default; virtual string draw() const = 0; };
struct Checkbox { virtual ~Checkbox() = default; virtual string mark() const = 0; };
struct ThemedButton final : Button {
    string theme; explicit ThemedButton(string t): theme(std::move(t)) {}
    string draw() const override { return theme + ":button"; }
};
struct ThemedCheckbox final : Checkbox {
    string theme; explicit ThemedCheckbox(string t): theme(std::move(t)) {}
    string mark() const override { return theme + ":checkbox"; }
};
struct WidgetFactory {
    virtual ~WidgetFactory() = default;
    virtual std::unique_ptr<Button> button() const = 0;
    virtual std::unique_ptr<Checkbox> checkbox() const = 0;
};
struct LightFactory final : WidgetFactory {
    std::unique_ptr<Button> button() const override { return std::make_unique<ThemedButton>("light"); }
    std::unique_ptr<Checkbox> checkbox() const override { return std::make_unique<ThemedCheckbox>("light"); }
};
struct DarkFactory final : WidgetFactory {
    std::unique_ptr<Button> button() const override { return std::make_unique<ThemedButton>("dark"); }
    std::unique_ptr<Checkbox> checkbox() const override { return std::make_unique<ThemedCheckbox>("dark"); }
};
string screen(const WidgetFactory& f) { return f.button()->draw() + "/" + f.checkbox()->mark(); }

int main() {
    check(screen(LightFactory{}) == "light:button/light:checkbox");
    check(screen(DarkFactory{}) == "dark:button/dark:checkbox");
    std::cout << "OK abstract-factory\n";
}
