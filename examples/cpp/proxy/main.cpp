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

struct Image { virtual ~Image() = default; virtual string read() = 0; };
struct RealImage final : Image { string read() override { return "pixels"; } };
class LazyImage final : public Image {
    std::unique_ptr<RealImage> real;
    int loads_ = 0;
public:
    int loads() const { return loads_; }
    string read() override {
        if (!real) { real = std::make_unique<RealImage>(); ++loads_; }
        return real->read();
    }
};

int main() {
    LazyImage image;
    check(image.loads() == 0); check(image.read() == "pixels");
    check(image.read() == "pixels" && image.loads() == 1);
    std::cout << "OK proxy\n";
}
