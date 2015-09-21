
use lex;

pub struct LexState {
    content: Vec<char>,
    current: usize,
    curline: usize,
    curcolumn: usize
}

impl LexState {
	fn new(s: &str) -> LexState {
		LexState {
			content: s.chars().collect::<Vec<char>>(),
			current: 0,
			curline: 1,
			curcolumn: 0
		}
	}

	fn len(&self) -> usize {
		self.content.len()
	}

	fn at_line_begin(&self) -> bool {
		self.curcolumn == 1
	}

	pub fn move_next(&mut self) -> bool {
		self.move_over(1)
	}

	#[inline(always)]
	pub fn move_over(&mut self, step: usize) -> bool {
		self.current += step;
		self.curcolumn += step;
		self.current < self.len()
	}

	fn next_is(&self, c: char) -> bool {
		if let Some(x) = self.peek() {
			return x == c;
		} else {
			false
		}
	}

	fn next_two_is(&self, c1: char, c2: char) -> bool {
		if let Some(x) = self.peek() {
			if x == c1 {
				if let Some(y) = self.peek_over(2) {
					return y == c2
				}
			}
		}
		false
	}

	fn next_is_any(&self, cs: &[char]) -> bool {
		if let Some(x) = self.peek() {
			for c in cs {
				if x == *c { return true; }
			}
			false
		} else {
			false
		}
	}

	#[inline(always)]
	pub fn current(&self) -> Option<char> {
		if self.current >= self.len() {
			None
		} else {
			Some(self.current_char())
		}
	}

	#[inline(always)]
	pub fn current_char(&self) -> char {
		self.content[self.current]
	}	

	fn peek(&self) -> Option<char> {
		self.peek_over(1)
	}

	#[inline(always)]
	fn peek_over(&self, a: usize) -> Option<char> {
		if self.current + a >= self.len() {
			None
		} else {
			Some(self.content[self.current + a])
		}
	}

	#[warn(dead_code)] 
	pub fn back(&mut self) {
		self.current -= 1;
		self.curcolumn -= 1;
	}
}

// For Python
impl LexState {
	fn is_python_indent_on(&self) -> bool {
		true
	}
}

#[inline(always)]
fn inc_line_number(ls: &mut LexState) {
	println!("Line from {:?}:{:?} changed", ls.curline, ls.curcolumn);
	ls.curline += 1;
	ls.curcolumn = 0;
}

#[inline(always)]
fn skip(ls: &mut LexState) {
	ls.move_next();
}

fn read_sym(ls: &mut LexState) -> String {
	let mut sym = String::new();
	//ls.move_next();
	while let Some(c) = ls.current() {
		match c {
			'_' | 'a'...'z' | 'A'...'Z' | '0'...'9' => { sym.push(c); }
			_ => { ls.back(); break}
		}
		ls.move_next();
	}
	sym
}

fn read_str(ls: &mut LexState, end: char) -> String {
	let mut ret = String::new();
	while let Some(c) = ls.current() {
		if c == '\\' {
			if let Some(n) = ls.peek() {
				if n == end {
					ret.push(n);
					ls.move_next();
				}
			}
		} else if (c == '"' && end == '"') {
			break;
		} else if (c == '\'' && end == '\'') {
			break;
		} else {
			ret.push(c)
		}

		ls.move_next();
	}

	ret
}

fn read_triquote_str(ls: &mut LexState, end: char) -> String {
	let mut ret = String::new();
	while let Some(c) = ls.current() {
		if c == end && ls.next_two_is(end, end) {
			ls.move_over(2);
			break;
		} else {
			ret.push(c)
		}

		ls.move_next();
	}
	
	ret
}

fn read_comment(ls: &mut LexState) -> String {
	let mut comment = String::new();
	ls.move_next();
	while let Some(c) = ls.current() {
		if c == '\n' {
			ls.back();
			break;
		}
		comment.push(c);
		ls.move_next();
	}
	comment
}

fn read_comment2(ls: &mut LexState) -> String {
	let mut comment = String::new();
	ls.move_next();
	while let Some(c) = ls.current() {
		if c == '*' && ls.peek() == Some('/') {
			ls.move_next();
			break;
		} else if c == '\n' {
			inc_line_number(ls);
		}

		comment.push(c);
		ls.move_next();
	}
	comment
}

fn read_indents(ls: &mut LexState) -> Option<usize> {
	let mut i = 0;
	
	while let Some(s) = ls.current() {
		match s {
			' ' => { i += 1 }
			'\t' => { return None }
			_ => { ls.back(); break; }
		}
		ls.move_next();
	}
	if i % 4 == 0 {
		Some(i / 4)
	} else {
		None
	}

}

fn is_keyword(sym: &str) -> bool {
	false
}

use lex::tokens::Token as Token;
use lex::tokens::TokenType as TokenType;

pub fn lex(s: &str) -> Vec<Token> {
	let mut tokens = Vec::<Token>::new();
	let mut ls = LexState::new(s);

	while let Some(c) = ls.current() {
		// println!("CHAR={:?}", c);
		match c {
			// New Line
			'\n' | '\r' => { 
				inc_line_number(&mut ls);
				tokens.push(Token{ token_type: TokenType::NewLine})
			}

			// White spaces
			' ' | '\t' => {
				if ls.at_line_begin() {
					if ls.is_python_indent_on() {
						if let Some(i) = read_indents(&mut ls) {
							tokens.push(Token{ token_type: TokenType::Indent(i) });
							println!("Indent={:?}", i);
						}
					}
				}
			} // Rust NOT support \f \v
			';' => { tokens.push(Token{ token_type: TokenType::Semicolon }); }
			',' => { tokens.push(Token{ token_type: TokenType::Comma }); }
			// String Literal
			'"' => {
				if ls.next_two_is('"', '"') {
					ls.move_over(3);
					let s = read_triquote_str(&mut ls, '"');
					tokens.push(Token{ token_type: TokenType::TriQuotedString(s, 0) });
				} else {
					ls.move_next();
					let s = read_str(&mut ls, '"');
					tokens.push(Token{ token_type: TokenType::DoubleQuotedString(s) });
				}

			}
			'\'' => {
				if ls.next_two_is('\'', '\'') {
					ls.move_over(3);
					let s = read_triquote_str(&mut ls, '\'');
					tokens.push(Token{ token_type: TokenType::TriQuotedString(s, 1) });
				} else {				
					ls.move_next();
					let s = read_str(&mut ls, '\'');
					tokens.push(Token{ token_type: TokenType::SingleQuotedString(s) });
				}
			}
			//
			'[' | ']' | '(' | ')' | '{' | '}' => {

			}

			':' => {
				if ls.next_is(':') {
					ls.move_next();
					tokens.push(Token{ token_type: TokenType::Colon2 });
				} else {
					tokens.push(Token{ token_type: TokenType::Colon });
				}
			}

			'=' => {
				if ls.next_is('=') {
					ls.move_next();
					tokens.push(Token{ token_type: TokenType::Equal });
				} else {
					tokens.push(Token{ token_type: TokenType::Assign });
				}
			}

			'#' => {
				let comment = read_comment(&mut ls);
				tokens.push(Token{ token_type: TokenType::ShellComment(comment) });
			}
			//------------------------------------
			'/' => {
				if ls.next_is('*') { /* comment */
					ls.move_next();
					let comment = read_comment2(&mut ls);
					tokens.push(Token{ token_type: TokenType::ClangComment(comment) });
				} else if ls.next_is('=') {	// a/=3
					ls.move_next();
				} else {	// 2/3
				}
			}

			'+' | '-' | '*' => {
				if ls.next_is_any(&['=']) {
					ls.move_next();
					println!("{:?}", "+=");
				} else {
					println!("OP{:?}", c);
				}
			}

			'_' | 'a'...'z' | 'A'...'Z' => {
				let sym = read_sym(&mut ls);
				if is_keyword(&sym) {
					tokens.push(Token{ token_type: TokenType::Keyword(sym) });
				} else {
					tokens.push(Token{ token_type: TokenType::Symbol(sym) });
				}
			}

			// Number TODO: BUG
			'.' | '0'...'9' => {
				if c == '0' && ls.peek() == Some('x') {
					ls.move_over(2);
					if let Some(hex) = lex::number::read_hex_number(&mut ls) {
						tokens.push(Token{ token_type: TokenType::Hex(hex) });
					} else {
						println!("Bad Hex Number Token!");
					}
		
					ls.back();
				} else {
					if let Some((number, is_float)) = lex::number::read_number(&mut ls) {
						if is_float {
							tokens.push(Token{ token_type: TokenType::Float(number) });
						}
						else {
							tokens.push(Token{ token_type: TokenType::Int(number) });
						}
					} else {
						println!("Bad Number Token!");
					}
					ls.back();
				}
			}

			// Symbol

			_ => {
				println!("Not handled{:?}", c);
			}
		}
		
		ls.move_next();
	}

	tokens
}
