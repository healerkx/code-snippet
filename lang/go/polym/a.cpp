#include <iostream>
using namespace std;

struct I {
	virtual void f() = 0;
};

struct Aa : I {
	void f();
};
struct Bb : I {
	void f();
};

void Aa::f() {
	cout<<"A";
}

void Bb::f() {
	cout<<"B";	
}

I* Get() {
	if (true) {
		return new Aa();
	} else {
		return new Bb();
	}
}

int main() {
	I* a = Get();
	a->f();
}
