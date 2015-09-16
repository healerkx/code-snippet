
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

	fn current(&self) -> Option<char> {
		if self.current + 1>= self.len() {
			None
		} else {
			Some(self.content[self.current])
		}
	}

	fn current_char(&self) -> char {
		self.content[self.current]
	}	

	fn peek(&self) -> Option<char> {
		if self.current + 1>= self.len() {
			None
		} else {
			Some(self.content[self.current + 1])
		}
	}

	fn back(&mut self) {
		self.current -= 1
	}
}

fn inc_line_number(ls: &mut LexState) {
	ls.curline += 1;
}

fn skip(ls: &mut LexState) {
	
}

pub fn lex(s: &str) {
	let mut ls = LexState::new(s);

	while let Some(c) = ls.current() {
		match c {
			// New Line
			'\n' | '\r' => { inc_line_number(&mut ls) }

			// White spaces
			' ' | '\t' => { skip(&mut ls) } // Rust NOT support \f \v

			'"' => {}
			'\'' => {}

			'=' => {
				if (ls.next_is_any(&['='])) {
					println!("{:?}", 222);
				} else {
					println!("{:?}", 333);
				}
			}

			_ => {}
		}
		ls.move_next();
	}
}

pub fn llex() {
	println!("{:?}", lex::number::is_valid_number());
}