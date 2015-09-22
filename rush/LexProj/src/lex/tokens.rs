
#[derive(Debug)]
pub enum TokenType {
	NewLine,
	Skip,
	BadToken,
	Int(String),
	Hex(String),
	Float(String),
	Indent(usize),
	ShellComment(String),
	ClangComment(String),
	StringLiteral(String, char),
	TriQuotedString(String, i32),
	Symbol(String),
	Keyword(String),
	Bracket(char),
	Arithmetic(String),
	ArithAssign(String),
	Equal,
	Assign,

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

