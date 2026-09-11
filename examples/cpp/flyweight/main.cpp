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

struct Style { const string font; explicit Style(string value): font(std::move(value)) {} };
class StylePool {
    std::map<string, std::shared_ptr<const Style>> cache;
public:
    std::shared_ptr<const Style> get(const string& font) {
        auto it = cache.find(font);
        if (it != cache.end()) return it->second;
        auto style = std::make_shared<const Style>(font); cache.emplace(font, style); return style;
    }
};
struct Glyph { char character; int x; std::shared_ptr<const Style> style; };

int main() {
    StylePool pool;
    Glyph a{'a', 1, pool.get("mono")}, b{'b', 8, pool.get("mono")};
    check(a.style == b.style); check(a.x != b.x);
    check(pool.get("serif") != a.style);
    std::cout << "OK flyweight\n";
}
