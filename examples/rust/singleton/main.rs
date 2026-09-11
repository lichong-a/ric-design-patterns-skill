use std::sync::OnceLock;

struct Settings { mode: &'static str }
static SETTINGS: OnceLock<Settings> = OnceLock::new();
fn shared_settings() -> &'static Settings { SETTINGS.get_or_init(|| Settings { mode: "demo" }) }

fn main() {
    assert!(std::ptr::eq(shared_settings(), shared_settings()));
    assert_eq!(shared_settings().mode, "demo");
    println!("OK singleton");
}
