
#[derive(Debug)]
pub enum TokenType {
	NewLine,
	Int(String),
	Hex(String),
	Float(String),
	Indent(usize),
	ShellComment(String),
	ClangComment(String),
	SingleQuotedString(String),
	DoubleQuotedString(String),
	TriQuotedString(String, i32),
	Symbol(String),
	Keyword(String),


	Equal,
	Assign,
	OpAssign,

	Comma,
	Colon,
	Colon2,
	Semicolon,
}

#[derive(Debug)]
pub struct Token {
	pub token_type: TokenType,

}


impl Token {
	fn to_str(&self) -> String {
		"".to_string()
	}
}

