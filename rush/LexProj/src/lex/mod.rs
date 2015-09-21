

mod lexstate;
mod number;
mod tokens;

pub fn test() {
	println!("Hello, world!");
	let v = lexstate::lex("
if c==-.e4 : #ddd
    a, b = \"hello\", 'world'/*ddd
aaa*/
	'''abcde'''
    if a == c:
        print(3)
    b = 0xff");


	let mut i = v.iter();
    while let Some(x) = i.next() {
    	println!("{:?}", x);
    }
    
	// number::is_valid_number();
}

