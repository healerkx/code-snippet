
/**
clang++ delegate.cpp -std=c++11 -stdlib=libc++
*/

#include <vector>
#include <functional>
#include <memory>


template<class ...T>
class Delegate
{
public:
	typedef std::function<void(T...)> f_t;


	Delegate(f_t f)
	{
		this->_functions.push_back(f);
	}

	void operator+=(f_t f)
	{
		this->_functions.push_back(f);
	}

	void operator()(T... args)
	{
		auto i = _functions.begin();
		for (; i != _functions.end(); i++)
		{
			(*i)(args...);
		}
	}

private:
	std::vector<f_t>	_functions;
};


void f1(int , char, const char*)
{
	printf("f1 invoked\n");
}

void f2(int , char, const char*)
{
	printf("f2 invoked\n");	
}

int main()
{
	Delegate<int, char, const char*> d(f1);
	d += f2;
	d(1, 'a', "hello");

	return 0;
}
