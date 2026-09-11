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

struct Channel { virtual ~Channel() = default; virtual string send(const string&) const = 0; };
struct EmailChannel final : Channel { string send(const string& s) const override { return "email:" + s; } };
struct SmsChannel final : Channel { string send(const string& s) const override { return "sms:" + s; } };
class Notice {
protected:
    const Channel& channel;
public:
    explicit Notice(const Channel& c): channel(c) {}
    virtual ~Notice() = default;
    virtual string deliver(const string& s) const { return channel.send(s); }
};
struct UrgentNotice final : Notice {
    using Notice::Notice;
    string deliver(const string& s) const override { return channel.send("!" + s); }
};

int main() {
    EmailChannel email; SmsChannel sms;
    check(Notice{email}.deliver("hi") == "email:hi");
    check(UrgentNotice{sms}.deliver("hi") == "sms:!hi");
    std::cout << "OK bridge\n";
}
