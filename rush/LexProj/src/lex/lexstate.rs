
use lex;

pub struct LexState {
    content: Vec<char>,
    current: usize,
}

impl LexState {
	fn new(s: &str) -> LexState {
		LexState {
			content: s.chars().collect::<Vec<char>>(),
			current: 0
		}
	}

	fn len(&self) -> usize {
		self.content.len()
	}

	fn current_char(&self) -> char {
		self.content[self.current]
	}

	fn next(&mut self) -> Option<char> {
		if self.current + 1 >= self.len() {
			None
		} else {
			let c = self.current_char();
			self.current += 1;
			Some(c)
		}
	}

	fn peek(&mut self) -> Option<char> {
		if self.current + 1 >= self.len() {
			None
		} else {
			Some(self.content[self.current + 1])
		}
	}

	fn back(&mut self) {
		self.current -= 1
	}
}

pub fn lex(s: &str) {
	let mut ls = LexState::new(s);

	while let Some(c) = ls.next() {
		match c {


			_ => {}
		}
	}
}

pub fn llex() {
	println!("{:?}", lex::number::is_valid_number());
}