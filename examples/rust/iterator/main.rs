struct Bag { values: Vec<i32> }
impl<'a> IntoIterator for &'a Bag {
    type Item = &'a i32;
    type IntoIter = std::slice::Iter<'a, i32>;
    fn into_iter(self) -> Self::IntoIter { self.values.iter() }
}

fn main() {
    let bag = Bag { values: vec![1, 2, 3] };
    let mut a = (&bag).into_iter(); let mut b = (&bag).into_iter();
    assert_eq!(a.next(), Some(&1)); assert_eq!(a.next(), Some(&2)); assert_eq!(b.next(), Some(&1));
    assert_eq!((&bag).into_iter().copied().sum::<i32>(), 6);
    let empty = Bag { values: vec![] }; assert_eq!((&empty).into_iter().next(), None);
    println!("OK iterator");
}
