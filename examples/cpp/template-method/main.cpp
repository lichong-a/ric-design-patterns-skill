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

class Importer {
protected:
    virtual string parse(string value) const = 0;
public:
    virtual ~Importer() = default;
    string run(string raw) const {
        const auto start = raw.find_first_not_of(" ");
        const auto end = raw.find_last_not_of(" ");
        raw = start == string::npos ? "" : raw.substr(start, end - start + 1);
        return "<" + parse(raw) + ">";
    }
};
struct UpperImporter final : Importer {
    string parse(string value) const override {
        for (char& c : value) if (c >= 'a' && c <= 'z') c = static_cast<char>(c - 'a' + 'A');
        return value;
    }
};

int main() {
    check(UpperImporter{}.run(" hello ") == "<HELLO>");
    check(UpperImporter{}.run("   ") == "<>");
    std::cout << "OK template-method\n";
}
