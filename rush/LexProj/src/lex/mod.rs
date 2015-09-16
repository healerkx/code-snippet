

mod lexstate;
mod number;

pub fn test() {
	println!("Hello, world!");
	lexstate::lex("==");
	number::is_valid_number();
}

