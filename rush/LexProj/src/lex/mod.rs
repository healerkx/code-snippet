

mod lexstate;
mod number;

pub fn test() {
	println!("Hello, world!");
	lexstate::lex("a==3, /* dddd */ b+= 2 # fffff");
	number::is_valid_number();
}

