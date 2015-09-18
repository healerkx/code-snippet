

mod lexstate;
mod number;

pub fn test() {
	println!("Hello, world!");
	lexstate::lex("if c==2 : #ddd
    a, b = \"hello\", 'world'/*ddd
aaa*/
    if a == c:
        print(3)
    b = 3");
	// number::is_valid_number();
}

