
use lex;

pub struct LexState {
    content: Vec<char>,
    current: usize,
    curline: usize,
}

impl LexState {
	fn new(s: &str) -> LexState {
		LexState {
			content: s.chars().collect::<Vec<char>>(),
			current: 0,
			curline: 1
		}
	}

	fn len(&self) -> usize {
		self.content.len()
	}

	fn move_next(&mut self) -> bool {
		self.current += 1;
		self.current < self.len()
	}

	fn next_is(&self, c: char) -> bool {
		if let Some(x) = self.peek() {
			println!("2{:?}", x);
			return x == c;
		} else {
			false
		}
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
	fn current(&self) -> Option<char> {
		if self.current>= self.len() {
			None
		} else {
			Some(self.current_char())
		}
	}

	#[inline(always)]
	fn current_char(&self) -> char {
		self.content[self.current]
	}	

	fn peek(&self) -> Option<char> {
		if self.current + 1 >= self.len() {
			None
		} else {
			Some(self.content[self.current + 1])
		}
	}
	/*
	fn back(&mut self) {
		self.current -= 1
	}
	*/
}

#[inline(always)]
fn inc_line_number(ls: &mut LexState) {
	ls.curline += 1;
}

#[inline(always)]
fn skip(ls: &mut LexState) {
	ls.move_next();
}

fn read_comment(ls: &mut LexState) -> String {
	let mut comment = String::new();
	ls.move_next();
	while let Some(c) = ls.current() {
		if c == '\n' {
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
			break;
		}
		comment.push(c);
		ls.move_next();
	}
	comment
}


pub fn lex(s: &str) {
	let mut ls = LexState::new(s);

	while let Some(c) = ls.current() {
		match c {
			// New Line
			'\n' | '\r' => { inc_line_number(&mut ls) }

			// White spaces
			' ' | '\t' => { } // Rust NOT support \f \v

			// String Literal
			'"' => {}
			'\'' => {}

			'=' => {
				if ls.next_is('=') {
					ls.move_next();
					println!("{:?}", "==");
				} else {
					
				}
			}

			'#' => { println!("comment={:?}", read_comment(&mut ls)) }
			//------------------------------------
			'/' => {
				if ls.next_is('*') { /* comment */
					ls.move_next();
					println!("comment={:?}", read_comment2(&mut ls))
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
					
				}
			}

			// Number

			// Symbol

			_ => {
				println!("Not handled{:?}", c);
			}
		}
		
		ls.move_next();
	}
}

pub fn llex() {
	println!("{:?}", lex::number::is_valid_number());
}