

mod lexstate;
mod number;
mod tokens;

pub fn test() {
	println!("Hello, world!");
	let v = lexstate::lex("if c==2 : #ddd
    a, b = \"hello\", 'world'/*ddd
aaa*/
	'''abcde'''
    if a == c:
        print(3)
    b = 3");
    println!("{:?}", v);
	// number::is_valid_number();
}

