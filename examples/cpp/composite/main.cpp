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

struct Item { virtual ~Item() = default; virtual int total() const = 0; };
struct LineItem final : Item {
    int price; explicit LineItem(int p): price(p) { if (p < 0) throw std::invalid_argument("price"); }
    int total() const override { return price; }
};
struct Bundle final : Item {
    std::vector<std::unique_ptr<Item>> children;
    void add(std::unique_ptr<Item> child) {
        if (!child) throw std::invalid_argument("null child");
        children.push_back(std::move(child));
    }
    int total() const override { int result = 0; for (const auto& x : children) result += x->total(); return result; }
};

int main() {
    Bundle root;
    check(root.total() == 0);
    root.add(std::make_unique<LineItem>(10));
    auto nested = std::make_unique<Bundle>();
    nested->add(std::make_unique<LineItem>(20));
    nested->add(std::make_unique<LineItem>(30));
    root.add(std::move(nested));
    check(root.total() == 60);
    std::cout << "OK composite\n";
}
