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

struct Report { string title; std::vector<string> sections; };
class ReportBuilder {
    string title_; std::vector<string> sections_;
public:
    ReportBuilder& title(string value) { title_ = std::move(value); return *this; }
    ReportBuilder& section(string value) { sections_.push_back(std::move(value)); return *this; }
    Report build() const {
        if (title_.empty()) throw std::invalid_argument("title required");
        return {title_, sections_};
    }
};

int main() {
    ReportBuilder b;
    expect_error([&]{ b.build(); });
    auto first = b.title("Design").section("Intent").build();
    b.section("Tests");
    check(first.sections.size() == 1 && b.build().sections.size() == 2);
    std::cout << "OK builder\n";
}
