
use std::fs::File;
use std::path::Path;
use std::collections::hash_map::HashMap;
use std::io::BufReader;
use std::io::prelude::*;

fn read_file_into_vec_char(filename: &str) -> Vec<char> {
    let file = File::open(Path::new(filename));
    if let Ok(mut h) = file {
        let mut contents = String::new();
        h.read_to_string(&mut contents);

        contents.chars().collect::<Vec<char>>()
    } else {
        vec![]  
    }
}

fn visit_vec_into_words(v: &Vec<char>, word_len: usize) -> HashMap<String, i32> {
    let mut words_map = HashMap::new();
    for x in v.windows(word_len) {
        let word : String = x.iter().cloned().collect();
        if let Some(c) = words_map.get_mut(&word) {
            *c += 1;
            continue;
        }

        words_map.insert(word, 1);
    }
    words_map
}

fn main() {

    let v = read_file_into_vec_char("foo.txt");

    // 单字出现次数统计
    let m1 = visit_vec_into_words(&v, 1);
    println!("{}", m1.len());

    // 2字词出现次数统计
    let m2 = visit_vec_into_words(&v, 2);
    for i in m2 {
        if i.1 > 4 {
            println!("{}:{}", i.0, i.1);
        }
    }
    
    // 3字词出现次数统计
    let m3 = visit_vec_into_words(&v, 3);
    for i in m3 {
        if i.1 > 4 {
            println!("{}:{}", i.0, i.1);
        }
    }

    // 4字词出现次数统计
    let m4 = visit_vec_into_words(&v, 4);
    for i in m4 {
        if i.1 > 4 {
            println!("{}:{}", i.0, i.1);
        }
    }
}
