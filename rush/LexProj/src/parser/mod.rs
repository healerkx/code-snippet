

use lex::tokens::TokenType as TokenType;

pub fn name() -> i32 {
    let a = (TokenType::Symbol("a".to_string()), TokenType::Equal, TokenType::Float("3.14".to_string()));

    match a {
       (TokenType::Symbol(a), TokenType::Equal, _) => println!("{}", a),
        _ => println!("Nothing matched"),
    }
    0
}
