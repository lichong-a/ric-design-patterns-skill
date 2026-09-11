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

struct Renderer { virtual ~Renderer() = default; virtual string render() const = 0; };
struct PlainRenderer final : Renderer { string render() const override { return "plain"; } };
struct JsonRenderer final : Renderer { string render() const override { return "json"; } };
class Publisher {
protected:
    virtual std::unique_ptr<Renderer> make() const = 0;
public:
    virtual ~Publisher() = default;
    string publish() const { return "published:" + make()->render(); }
};
struct PlainPublisher final : Publisher {
    std::unique_ptr<Renderer> make() const override { return std::make_unique<PlainRenderer>(); }
};
struct JsonPublisher final : Publisher {
    std::unique_ptr<Renderer> make() const override { return std::make_unique<JsonRenderer>(); }
};

int main() {
    check(PlainPublisher{}.publish() == "published:plain");
    check(JsonPublisher{}.publish() == "published:json");
    std::cout << "OK factory-method\n";
}
