use std::collections::HashMap;

type Context = HashMap<String, i32>;
trait Expr { fn evaluate(&self, context: &Context) -> Result<i32, String>; }
struct Literal { value: i32 }
impl Expr for Literal { fn evaluate(&self, _: &Context) -> Result<i32, String> { Ok(self.value) } }
struct Variable { name: String }
impl Expr for Variable {
    fn evaluate(&self, context: &Context) -> Result<i32, String> {
        context.get(&self.name).copied().ok_or_else(|| format!("unknown variable: {}", self.name))
    }
}
struct Add { left: Box<dyn Expr>, right: Box<dyn Expr> }
impl Expr for Add {
    fn evaluate(&self, context: &Context) -> Result<i32, String> {
        self.left.evaluate(context)?.checked_add(self.right.evaluate(context)?).ok_or_else(|| "overflow".to_owned())
    }
}

fn main() {
    let expr = Add { left: Box::new(Variable { name: "x".into() }), right: Box::new(Literal { value: 2 }) };
    assert_eq!(expr.evaluate(&HashMap::from([("x".into(), 3)])).expect("known variable"), 5);
    assert!(expr.evaluate(&HashMap::new()).is_err());
    let large = Add { left: Box::new(Literal { value: i32::MAX }), right: Box::new(Literal { value: 1 }) };
    assert!(large.evaluate(&HashMap::new()).is_err());
    println!("OK interpreter");
}
