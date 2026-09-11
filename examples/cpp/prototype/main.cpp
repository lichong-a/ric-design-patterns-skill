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

struct Document {
    string title; std::vector<std::vector<string>> paragraphs;
    Document clone() const { return *this; }
};

int main() {
    Document original{"Design", {{"first"}}};
    auto copy = original.clone();
    copy.paragraphs[0].push_back("second");
    check(original.paragraphs[0].size() == 1);
    check(copy.paragraphs[0].size() == 2);
    std::cout << "OK prototype\n";
}
