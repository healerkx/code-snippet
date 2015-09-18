
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
		self.current += 1;
		self.curcolumn += 1;
		self.current < self.len()
	}

	pub fn move_on(&mut self, step: usize) -> bool {
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
		if self.current + 1 >= self.len() {
			None
		} else {
			Some(self.content[self.current + 1])
		}
	}

	#[warn(dead_code)] 
	pub fn back(&mut self) {
		self.current -= 1;
		self.curcolumn -= 1;
	}

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


pub fn lex(s: &str) {
	let mut ls = LexState::new(s);

	while let Some(c) = ls.current() {
		// println!("CHAR={:?}", c);
		match c {
			// New Line
			'\n' | '\r' => { inc_line_number(&mut ls) }

			// White spaces
			' ' | '\t' => {
				if ls.at_line_begin() {
					if ls.is_python_indent_on() {
						println!("Indent={:?}", read_indents(&mut ls));
					}
				}
			} // Rust NOT support \f \v
			';' => {}
			',' => {}
			// String Literal
			'"' => {
				ls.move_next();
				println!("String1={:?}", read_str(&mut ls, '"'));
			}
			'\'' => {
				ls.move_next();
				println!("String2={:?}", read_str(&mut ls, '\''));
			}
			//
			'[' | ']' | '(' | ')' | '{' | '}' => {

			}

			':' => {
				if ls.next_is(':') {
					ls.move_next();
					println!("{:?}", "::");
				} else {
					
				}
			}

			'=' => {
				if ls.next_is('=') {
					ls.move_next();
					
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
					println!("OP{:?}", c);
				}
			}

			'_' | 'a'...'z' | 'A'...'Z' => {
				println!("Sym={:?}", read_sym(&mut ls));
			}

			// Number
			'.' | '0'...'9' => {
				if c == '0' && ls.peek() == Some('x') {
					ls.move_on(2);
					println!("Hex Number={:?}", lex::number::read_hex_number(&mut ls));
					ls.back();
				} else {
					println!("Number={:?}", lex::number::read_number(&mut ls));
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
}
