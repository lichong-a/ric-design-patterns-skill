trait Image { fn read(&mut self) -> &'static str; }
struct RealImage;
impl Image for RealImage { fn read(&mut self) -> &'static str { "pixels" } }
#[derive(Default)]
struct LazyImage { real: Option<RealImage>, loads: usize }
impl Image for LazyImage {
    fn read(&mut self) -> &'static str {
        if self.real.is_none() { self.real = Some(RealImage); self.loads += 1; }
        self.real.as_mut().expect("initialized immediately above").read()
    }
}

fn main() {
    let mut image = LazyImage::default();
    assert_eq!(image.loads, 0);
    assert_eq!(image.read(), "pixels"); assert_eq!(image.read(), "pixels");
    assert_eq!(image.loads, 1);
    println!("OK proxy");
}
