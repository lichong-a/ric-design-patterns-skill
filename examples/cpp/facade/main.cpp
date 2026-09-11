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

struct Inventory {
    string reserve(int quantity) const {
        if (quantity <= 0) throw std::invalid_argument("positive quantity required");
        return "reserved:" + std::to_string(quantity);
    }
};
struct Receipts { string create(const string& reservation) const { return "receipt:" + reservation; } };
struct Checkout {
    Inventory inventory; Receipts receipts;
    string place(int quantity) const { return receipts.create(inventory.reserve(quantity)); }
};

int main() {
    Checkout checkout;
    check(checkout.place(2) == "receipt:reserved:2");
    expect_error([&]{ checkout.place(0); });
    std::cout << "OK facade\n";
}
