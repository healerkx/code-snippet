
// clang++ tuple.cpp -std=c++11 -stdlib=libc++

#include <iostream>
#include <tuple> 
using namespace std;

int main()
{
	tuple<int, int, const char*> t(0, 0, "hello");

	std::cout
		<< sizeof(std::tuple_element<2, decltype(t)>::type)	// Get the Nth Type within a tuple
		<< endl
		<< get<2>(t) // Get the Nth Value.
		<< endl;

	return 0;
}