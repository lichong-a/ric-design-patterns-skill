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

using Context = std::map<string, int>;
struct Expr { virtual ~Expr() = default; virtual int eval(const Context&) const = 0; };
struct Literal final : Expr {
    int value; explicit Literal(int v): value(v) {}
    int eval(const Context&) const override { return value; }
};
struct Variable final : Expr {
    string name; explicit Variable(string n): name(std::move(n)) {}
    int eval(const Context& c) const override { return c.at(name); }
};
struct Add final : Expr {
    std::unique_ptr<Expr> left, right;
    Add(std::unique_ptr<Expr> l, std::unique_ptr<Expr> r): left(std::move(l)), right(std::move(r)) {
        if (!left || !right) throw std::invalid_argument("operands");
    }
    int eval(const Context& c) const override { return left->eval(c) + right->eval(c); }
};

int main() {
    Add expr{std::make_unique<Variable>("x"), std::make_unique<Literal>(2)};
    check(expr.eval({{"x", 3}}) == 5);
    expect_error([&]{ expr.eval({}); });
    std::cout << "OK interpreter\n";
}
