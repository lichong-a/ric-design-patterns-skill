trait Channel { fn send(&self, value: &str) -> String; }
struct EmailChannel;
impl Channel for EmailChannel { fn send(&self, value: &str) -> String { format!("email:{value}") } }
struct SmsChannel;
impl Channel for SmsChannel { fn send(&self, value: &str) -> String { format!("sms:{value}") } }
trait Notice {
    fn channel(&self) -> &dyn Channel;
    fn message(&self, value: &str) -> String;
    fn deliver(&self, value: &str) -> String { self.channel().send(&self.message(value)) }
}
struct PlainNotice { channel: Box<dyn Channel> }
impl Notice for PlainNotice {
    fn channel(&self) -> &dyn Channel { self.channel.as_ref() }
    fn message(&self, value: &str) -> String { value.to_owned() }
}
struct UrgentNotice { channel: Box<dyn Channel> }
impl Notice for UrgentNotice {
    fn channel(&self) -> &dyn Channel { self.channel.as_ref() }
    fn message(&self, value: &str) -> String { format!("!{value}") }
}

fn main() {
    let plain = PlainNotice { channel: Box::new(EmailChannel) };
    let urgent = UrgentNotice { channel: Box::new(SmsChannel) };
    assert_eq!(plain.deliver("hi"), "email:hi");
    assert_eq!(urgent.deliver("hi"), "sms:!hi");
    println!("OK bridge");
}
