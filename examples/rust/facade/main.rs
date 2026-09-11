struct Inventory;
impl Inventory {
    fn reserve(&self, quantity: u32) -> Result<String, &'static str> {
        if quantity == 0 { return Err("positive quantity required"); }
        Ok(format!("reserved:{quantity}"))
    }
}
struct Receipts;
impl Receipts { fn create(&self, reservation: &str) -> String { format!("receipt:{reservation}") } }
struct Checkout { inventory: Inventory, receipts: Receipts }
impl Checkout {
    fn place(&self, quantity: u32) -> Result<String, &'static str> {
        let reservation = self.inventory.reserve(quantity)?;
        Ok(self.receipts.create(&reservation))
    }
}

fn main() {
    let checkout = Checkout { inventory: Inventory, receipts: Receipts };
    assert_eq!(checkout.place(2).expect("valid quantity"), "receipt:reserved:2");
    assert!(checkout.place(0).is_err());
    println!("OK facade");
}
