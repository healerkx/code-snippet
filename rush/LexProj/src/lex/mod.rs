

mod lexstate;
mod number;

pub fn test() {
	println!("Hello, world!");
	lexstate::lex("if c==2: #ddd
    a = c/*ddd
aaa*/
    b = 3");
	// number::is_valid_number();
}

