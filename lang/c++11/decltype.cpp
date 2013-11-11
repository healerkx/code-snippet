
#include <map>
#include <string>
#include <iostream>
#include <typeinfo>
using namespace std;

class HttpStream
{

};

class HttpResponse
{
public:
	HttpStream* GetStream()
	{
		return nullptr;
	}
};

class HttpRequest
{
public:
	HttpResponse* GetResponse()
	{
		return nullptr;
	}
};

template<class T1>
auto GetStream(T1* req) -> decltype(req->GetResponse()->GetStream())
{
	decltype(req->GetResponse()->GetStream()) r;
	return r;
}


void simple_usage()
{
	string a = "hello";
	decltype(a) b = "world";

	cout<< typeid(a).name()<<endl;
	cout<< typeid(b).name()<<endl;
}



int main(int argc, char const *argv[])
{
	simple_usage();

	auto s = GetStream(new HttpRequest());
	cout<< typeid(s).name()<<endl;
	return 0;
}