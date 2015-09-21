
use lex::lexstate::LexState;

pub fn read_int(ls: &mut LexState) -> String {
	let mut number = String::new();
	while let Some(c) = ls.current() {
		match c {
			'0'...'9' => { number.push(c) }
			_ => { break }
		}
		ls.move_next();
	}
	number
}

pub fn read_hex_number(ls: &mut LexState) -> Option<String> {
	let mut hex = "0x".to_string();
	while let Some(c) = ls.current() {
		match c {
			'0'...'9' | 'a'...'f' | 'A'...'F' => { hex.push(c) }
			_ => { break }
		}
		ls.move_next();
	}

	if let Some(e) = ls.current() {
		match e {
			'.' | '$' | '_' | 'a'...'z' | 'A'...'Z' => {
				return None
			}
			_ => {}
		}
	}
	Some(hex)
}

pub fn read_number(ls: &mut LexState) -> Option<(String, bool)> {
	let mut is_float = false;

	let mut number = read_int(ls);
	let has_int_part = number.len() > 0;
	let mut has_decimal_part = false;
	if let Some(d) = ls.current() {
		if d == '.' {
			number.push('.');
			ls.move_next();
			is_float = true;
		}
	}
	
	if is_float {
		let b = read_int(ls);
		if b.len() > 0 {
			has_decimal_part = true;
			number = number + &b;
		}
	}

	if !has_int_part && !has_decimal_part {
		return None;
	}

	if let Some(c) = ls.current() {
		if c == 'e' || c == 'E' {
			number.push(c);
			ls.move_next();

			if let Some(c) = ls.current() {
				match c {
					'+' | '-' => {
						number.push(c);
						ls.move_next();
						let e = read_int(ls);
						is_float = true;
						number = number + &e;
					}

					'0'...'9' => {
						let e = read_int(ls);
						is_float = true;
						number = number + &e;
					}
					_ => { return None }
				}
			}
		}
	}

	if let Some(e) = ls.current() {
		match e {
			'.' | '$' | '_' | 'a'...'z' | 'A'...'Z' => {
				return None
			}
			_ => {}
		}
	}

	Some((number, is_float))
}
