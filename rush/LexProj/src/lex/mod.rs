

mod lexstate;
mod number;

pub fn test() {
	println!("Hello, world!");
	lexstate::lex("a==1, b+=2");
	number::is_valid_number();
}

