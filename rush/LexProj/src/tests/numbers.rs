
use lex;

use lex::tokens::Token as Token;
use lex::tokens::TokenType as TokenType;

#[test]
fn case_dec_integer() {
	let i = lex::lexstate::lex("234");
	let a = &i[0];

	match &a.token_type {
		&TokenType::Int(ref n) => {
			assert_eq!(n, "234");
		}
		_ => { assert!(false); }
	}
}

#[test]
fn case_float1() {
	let i = lex::lexstate::lex("234.5");
	let a = &i[0];

	match &a.token_type {
		&TokenType::Float(ref n) => {
			assert_eq!(n, "234.5");
		}
		_ => { assert!(false); }
	}
}

#[test]
fn case_float2() {
	let i = lex::lexstate::lex("234.");
	let a = &i[0];

	match &a.token_type {
		&TokenType::Float(ref n) => {
			assert_eq!(n, "234.");
		}
		_ => { assert!(false); }
	}
}


#[test]
fn case_float3() {
	let i = lex::lexstate::lex(".12");
	let a = &i[0];

	match &a.token_type {
		&TokenType::Float(ref n) => {
			assert_eq!(n, ".12");
		}
		_ => { assert!(false); }
	}
}

#[test]
fn case_hex() {
	let i = lex::lexstate::lex("0x123f");
	let a = &i[0];

	match &a.token_type {
		&TokenType::Hex(ref n) => {
			assert_eq!(n, "0x123f");
		}
		_ => { assert!(false); }
	}
}