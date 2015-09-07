
fn sort(v: &mut Vec<i32>, l: usize, h: usize)
{
	if l >= h { return; }
	let m = v[h];
	let mut a = l;
	let mut b = h;

	loop
	{
		while v[a] < m { 
			a += 1;
		}

		b -= 1;
		while v[b] > m {
			b -= 1;
			if b == l { break; }
		}

		if a >= b { break; }
		v.swap(a, b);
		
	}
	
	v.swap(a, h);
	
	if a > 0 && a - 1 >= l {
		sort(v, l, a - 1);
	}
	sort(v, a + 1, h);
}

fn qsort(v: &mut Vec<i32>)
{
	let len = v.len();
	sort(v, 0, len - 1);
}

fn main() {
	
	let mut v = vec![10, 3, 4, 1, 5, 2, 5, 6, 7, 9, 8, 9];
	qsort(&mut v);

	println!("{:?}", v);
}