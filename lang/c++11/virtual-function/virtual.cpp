
#include <stdio.h>
#include "../pprint.h"

////////////////////////////////////////////
// Basic
class Base1
{
public:
	virtual void foo1()
	{
		printf("Base1::foo1\n");
	}

	virtual void foo2()
	{
		printf("Base1::foo2\n");
	}
};

class Base2
{
public:
	virtual void foo3()
	{
		printf("Base2::foo3\n");
	}

	virtual void foo4()
	{
		printf("Base2::foo4\n");
	}
};


class Derived1 : public Base1, public Base2
{
public:
	virtual void foo1()
	{
		/* override is a context keyword */
		int override = 1;
		printf("Derived1::foo1\n");
	}

	/* So override is optional */
	virtual void foo2() override
	{
		printf("Derived1::foo2\n");
	}

	virtual void foo3()
	{
		printf("Derived1::foo3\n");
	}

	virtual void foo4() final
	{
		printf("Derived1::foo4\n");
	}
};
////////////////////////////////////////////

/* Can NOT compile. For foo4 marked as 'final'
class Derived2 : public Derived1
{
	void foo4()
	{
	}
};
*/


int main(int argc, char const *argv[])
{
	Pretty pretty;
	pretty.select(KRED);
	// Invoke virtual function.
	Derived1* d = new Derived1();
	Base1* b = d;
	b->foo1();
	b->foo2();

	pretty.select(KGRN);
	// p0 would offset sizeof(Base1)
	Base2* p0 = (Base2*)d;
	p0->foo3();
	p0->foo4();

	pretty.select(KRED);
	// p1 would not move by offset
	Base2* p1 = (Base2*)b;
	p1->foo3();
	p1->foo4();

	pretty.select(KGRN);
	// p2 would move by offset.
	Base2* p2 = dynamic_cast<Base2*>(b);
	p2->foo3();
	p2->foo4();

	
	// Can NOT be compiled
	/*
	Base2* p2 = static_cast<Base2*>(b);
	p2->foo3();
	p2->foo4();
	*/

	return 0;
}