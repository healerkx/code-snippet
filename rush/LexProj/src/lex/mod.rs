

mod lexstate;
mod number;

pub fn test() {
	println!("Hello, world!");
	lexstate::lex("a_3b==3, /* dddd */ {_b+= 2;} # fffff");
	number::is_valid_number();
}

