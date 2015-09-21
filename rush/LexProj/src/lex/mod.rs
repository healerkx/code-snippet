

mod lexstate;
mod number;
mod tokens;


use lex::tokens::Token as Token;
pub fn print_tokens(tokens: &Vec<Token>) {
    let mut i = tokens.iter();
    while let Some(x) = i.next() {
        println!("{:?}", x);
    }
}

pub fn test() {
	println!("Hello, world!");
	let v = lexstate::lex("
if c==-.5e4 : #ddd
    a, b = \"hello\", 'world'/*ddd
    aaa*/
	'''abcde'''
    if a == c: 
        print(3)
    b = 0xff");

    print_tokens(&v);

    
	// number::is_valid_number();
}

