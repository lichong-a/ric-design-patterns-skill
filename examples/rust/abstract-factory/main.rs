trait Button { fn draw(&self) -> String; }
trait Checkbox { fn mark(&self) -> String; }
struct ThemedButton { theme: &'static str }
impl Button for ThemedButton { fn draw(&self) -> String { format!("{}:button", self.theme) } }
struct ThemedCheckbox { theme: &'static str }
impl Checkbox for ThemedCheckbox { fn mark(&self) -> String { format!("{}:checkbox", self.theme) } }
trait WidgetFactory { fn button(&self) -> Box<dyn Button>; fn checkbox(&self) -> Box<dyn Checkbox>; }
struct LightFactory;
impl WidgetFactory for LightFactory {
    fn button(&self) -> Box<dyn Button> { Box::new(ThemedButton { theme: "light" }) }
    fn checkbox(&self) -> Box<dyn Checkbox> { Box::new(ThemedCheckbox { theme: "light" }) }
}
struct DarkFactory;
impl WidgetFactory for DarkFactory {
    fn button(&self) -> Box<dyn Button> { Box::new(ThemedButton { theme: "dark" }) }
    fn checkbox(&self) -> Box<dyn Checkbox> { Box::new(ThemedCheckbox { theme: "dark" }) }
}
fn screen(f: &dyn WidgetFactory) -> String { format!("{}/{}", f.button().draw(), f.checkbox().mark()) }

fn main() {
    assert_eq!(screen(&LightFactory), "light:button/light:checkbox");
    assert_eq!(screen(&DarkFactory), "dark:button/dark:checkbox");
    println!("OK abstract-factory");
}
