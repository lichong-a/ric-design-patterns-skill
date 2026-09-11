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

struct LegacySensor { int centimeters() const { return 250; } };
struct MeterReader { virtual ~MeterReader() = default; virtual double meters() const = 0; };
struct SensorAdapter final : MeterReader {
    LegacySensor sensor;
    double meters() const override { return sensor.centimeters() / 100.0; }
};

int main() {
    SensorAdapter a;
    const MeterReader& reader = a;
    check(reader.meters() == 2.5);
    std::cout << "OK adapter\n";
}
