export {};

function check(condition: boolean, message = "contract failed"): void {
  if (!condition) throw new Error(message);
}
function expectThrows(action: () => unknown): void {
  let failed = false;
  try { action(); } catch { failed = true; }
  check(failed, "expected an error");
}

interface Channel { send(text: string): string; }
class EmailChannel implements Channel {
  send(text: string): string { return "email:" + text; }
}
class SmsChannel implements Channel {
  send(text: string): string { return "sms:" + text; }
}
class Notice {
  constructor(protected readonly channel: Channel) {}
  send(text: string): string { return this.channel.send(text); }
}
class UrgentNotice extends Notice {
  send(text: string): string { return this.channel.send("!" + text); }
}

check(new Notice(new EmailChannel()).send("ready") === "email:ready");
check(new Notice(new SmsChannel()).send("ready") === "sms:ready");
check(new UrgentNotice(new EmailChannel()).send("ready") === "email:!ready");
check(new UrgentNotice(new SmsChannel()).send("ready") === "sms:!ready");
console.log("OK bridge");
