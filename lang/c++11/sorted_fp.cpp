// sorted.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"


#include <vector>
#include <algorithm>
#include <iterator>
using namespace std;

template<typename T>
vector<T> operator +(vector<T>& op1, vector<T>& op2)
{
	vector<T> r;
	copy(begin(op1), end(op1), back_inserter(r));
	copy(begin(op2), end(op2), back_inserter(r));
	return move(r);
}

vector<int> sorted(vector<int> const& a)
{
	if (a.size() <= 1)
		return a;
	vector<int> v1, v2, v3;
	int k = a[0];
	copy_if(begin(a), end(a), back_inserter(v1), [&k](auto x) { return x < k; });
	copy_if(begin(a), end(a), back_inserter(v2), [&k](auto x) { return x == k; });
	copy_if(begin(a), end(a), back_inserter(v3), [&k](auto x) { return x > k; });

	auto r = sorted(v1) + sorted(v2) + sorted(v3);
	return move(r);
}


int _tmain(int argc, _TCHAR* argv[])
{

	vector<int> a = { 2, 3, 1, 6, 4, 5, 9, 8 };
	a = sorted(a);

	return 0;
}

