import Foundation

func check(_ condition: @autoclosure () -> Bool) {
    precondition(condition(), "check failed")
}
enum DemoError: Error { case invalid(String) }
func expectError(_ action: () throws -> Void) {
    var failed = false
    do { try action() } catch { failed = true }
    check(failed)
}

protocol Channel { func send(_ value: String) -> String }
struct EmailChannel: Channel { func send(_ value: String) -> String { "email:" + value } }
struct SmsChannel: Channel { func send(_ value: String) -> String { "sms:" + value } }
class Notice {
    let channel: any Channel
    init(_ channel: any Channel) { self.channel = channel }
    func deliver(_ value: String) -> String { channel.send(value) }
}
final class UrgentNotice: Notice {
    override func deliver(_ value: String) -> String { channel.send("!" + value) }
}

check(Notice(EmailChannel()).deliver("hi") == "email:hi")
check(UrgentNotice(SmsChannel()).deliver("hi") == "sms:!hi")
print("OK bridge")
