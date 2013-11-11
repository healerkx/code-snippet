
#include <cstddef>
#include <stdio.h>
using namespace std;

void func(nullptr_t null)
{
	printf("%p\n", null);
}

int main(int argc, char const *argv[])
{
	int* p = nullptr;
	// Can NOT compile.
	// func(p);
	func(nullptr);
	return 0;
}