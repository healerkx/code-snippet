

mod lexstate;
mod number;

pub fn test() {
	println!("Hello, world!");
	lexstate::llex();
	number::is_valid_number();
}

