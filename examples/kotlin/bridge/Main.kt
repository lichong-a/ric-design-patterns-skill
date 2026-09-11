package patterns.bridge

fun expectError(action: () -> Unit) {
    var failed = false
    try { action() } catch (_: RuntimeException) { failed = true }
    check(failed)
}

interface Channel { fun send(value: String): String }
class EmailChannel : Channel { override fun send(value: String) = "email:$value" }
class SmsChannel : Channel { override fun send(value: String) = "sms:$value" }
open class Notice(protected val channel: Channel) {
    open fun deliver(value: String) = channel.send(value)
}
class UrgentNotice(channel: Channel) : Notice(channel) {
    override fun deliver(value: String) = channel.send("!$value")
}

fun main() {
    check(Notice(EmailChannel()).deliver("hi") == "email:hi")
    check(UrgentNotice(SmsChannel()).deliver("hi") == "sms:!hi")
    println("OK bridge")
}
