struct Pricing { rule: Box<dyn Fn(i32) -> i32> }
impl Pricing {
    fn quote(&self, base: i32) -> Result<i32, &'static str> {
        if base < 0 { return Err("base"); }
        Ok((self.rule)(base))
    }
}
fn discount(amount: i32) -> impl Fn(i32) -> i32 { move |base| base.saturating_sub(amount).max(0) }

fn main() {
    let mut pricing = Pricing { rule: Box::new(discount(10)) };
    assert_eq!(pricing.quote(100).expect("valid base"), 90);
    pricing.rule = Box::new(discount(20));
    assert_eq!(pricing.quote(100).expect("valid base"), 80);
    assert_eq!(pricing.quote(5).expect("valid base"), 0);
    assert!(pricing.quote(-1).is_err());
    println!("OK strategy");
}
