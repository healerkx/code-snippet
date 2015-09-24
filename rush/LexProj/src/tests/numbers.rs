
use lex;

use lex::tokens::Token as Token;
use lex::tokens::TokenType as TokenType;

#[test]
fn case_dec_integer() {
	let i = lex::lexstate::lex("234");
	match &i[0].token_type {
		&TokenType::Int(ref n) => {
			assert_eq!(n, "234");
		}
		_ => { assert!(false); }
	}
}

#[test]
fn case_float1() {
	let i = lex::lexstate::lex("234.5");
	match &i[0].token_type {
		&TokenType::Float(ref n) => {
			assert_eq!(n, "234.5");
		}
		_ => { assert!(false); }
	}
}

#[test]
fn case_float2() {
	let i = lex::lexstate::lex("234.");
	match &i[0].token_type {
		&TokenType::Float(ref n) => {
			assert_eq!(n, "234.");
		}
		_ => { assert!(false); }
	}
}


#[test]
fn case_float3() {
	let i = lex::lexstate::lex(".12");
	match &i[0].token_type {
		&TokenType::Float(ref n) => {
			assert_eq!(n, ".12");
		}
		_ => { assert!(false); }
	}
}

#[test]
fn case_e_float1() {
	let i = lex::lexstate::lex(".12e33");
	match &i[0].token_type {
		&TokenType::Float(ref n) => {
			assert_eq!(n, ".12e33");
		}
		_ => { assert!(false); }
	}
}

#[test]
fn case_e_float2() {
	let i = lex::lexstate::lex("1.e+4");
	match &i[0].token_type {
		&TokenType::Float(ref n) => {
			assert_eq!(n, "1.e+4");
		}
		_ => { assert!(false); }
	}
}


#[test]
fn case_e_float3() {
	let i = lex::lexstate::lex("1.2e3");
	match &i[0].token_type {
		&TokenType::Float(ref n) => {
			assert_eq!(n, "1.2e3");
		}
		_ => { assert!(false); }
	}
}

#[test]
fn case_hex() {
	let i = lex::lexstate::lex("0x123f");
	match &i[0].token_type {
		&TokenType::Hex(ref n) => {
			assert_eq!(n, "0x123f");
		}
		_ => { assert!(false); }
	}
}