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

struct TextNode; struct NumberNode;
struct NodeVisitor {
    virtual ~NodeVisitor() = default;
    virtual string visit_text(const TextNode&) const = 0;
    virtual string visit_number(const NumberNode&) const = 0;
};
struct Node { virtual ~Node() = default; virtual string accept(const NodeVisitor&) const = 0; };
struct TextNode final : Node {
    string value; explicit TextNode(string v): value(std::move(v)) {}
    string accept(const NodeVisitor& v) const override { return v.visit_text(*this); }
};
struct NumberNode final : Node {
    int value; explicit NumberNode(int v): value(v) {}
    string accept(const NodeVisitor& v) const override { return v.visit_number(*this); }
};
struct RenderVisitor final : NodeVisitor {
    string visit_text(const TextNode& n) const override { return "text:" + n.value; }
    string visit_number(const NumberNode& n) const override { return "number:" + std::to_string(n.value); }
};

int main() {
    RenderVisitor visitor;
    check(TextNode{"a"}.accept(visitor) == "text:a");
    check(NumberNode{7}.accept(visitor) == "number:7");
    std::cout << "OK visitor\n";
}
