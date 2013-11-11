
#include <map>
#include <string>
#include <iostream>
#include <typeinfo>
using namespace std;

void func(map<int, string> const& m)
{
	auto i = m.begin();

	cout<< typeid(i).name() << endl;
}



int main(int argc, char const *argv[])
{
	map<int, string> m;

	map<int, string>::iterator i1 = m.begin();


	auto i2 = m.begin();

	cout<< (typeid(i1) == typeid(i2))
		<< endl;


	func(m);
	return 0;
}