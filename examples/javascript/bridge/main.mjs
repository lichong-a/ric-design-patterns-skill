function check(condition, message = "contract failed") {
    if (!condition)
        throw new Error(message);
}
function expectThrows(action) {
    let failed = false;
    try {
        action();
    }
    catch {
        failed = true;
    }
    check(failed, "expected an error");
}
class EmailChannel {
    send(text) { return "email:" + text; }
}
class SmsChannel {
    send(text) { return "sms:" + text; }
}
class Notice {
    channel;
    constructor(channel) {
        this.channel = channel;
    }
    send(text) { return this.channel.send(text); }
}
class UrgentNotice extends Notice {
    send(text) { return this.channel.send("!" + text); }
}
check(new Notice(new EmailChannel()).send("ready") === "email:ready");
check(new Notice(new SmsChannel()).send("ready") === "sms:ready");
check(new UrgentNotice(new EmailChannel()).send("ready") === "email:!ready");
check(new UrgentNotice(new SmsChannel()).send("ready") === "sms:!ready");
console.log("OK bridge");
export {};
