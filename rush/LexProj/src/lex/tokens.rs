
#[derive(Debug)]
pub enum TokenType {
	NewLine,
	Int(i64),
	Hex(i64),
	Float(f64),
	Indent(usize),
	ShellComment(String),
	ClangComment(String),
	Symbol(String),
	Keyword(String)
}

#[derive(Debug)]
pub struct Token {
	pub token_type: TokenType,

}

