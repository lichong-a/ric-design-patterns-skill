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

struct Text { virtual ~Text() = default; virtual string render() const = 0; };
struct PlainText final : Text { string render() const override { return "hi"; } };
struct PrefixText final : Text {
    std::unique_ptr<Text> inner;
    explicit PrefixText(std::unique_ptr<Text> t): inner(std::move(t)) { if (!inner) throw std::invalid_argument("inner"); }
    string render() const override { return "!" + inner->render(); }
};
struct BracketText final : Text {
    std::unique_ptr<Text> inner;
    explicit BracketText(std::unique_ptr<Text> t): inner(std::move(t)) { if (!inner) throw std::invalid_argument("inner"); }
    string render() const override { return "[" + inner->render() + "]"; }
};

int main() {
    BracketText a{std::make_unique<PrefixText>(std::make_unique<PlainText>())};
    PrefixText b{std::make_unique<BracketText>(std::make_unique<PlainText>())};
    check(a.render() == "[!hi]"); check(b.render() == "![hi]");
    std::cout << "OK decorator\n";
}
