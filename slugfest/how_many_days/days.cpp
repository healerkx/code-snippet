// ConsoleApplication1.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <string>
#include <algorithm>

using namespace std;

#define is_leap(x) ((x % 4 == 0 && x % 100 != 0) || x % 400 == 0)

void addOneMonth(int& y, int& m)
{
	y += (m == 12) ? (m = 1, 1) : (++m, 0);
}

int countDay(int y, int m)
{
	int e[] = { 29, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
	m = (is_leap(y) && m == 2) ? 0 : m;
	return e[m];
}

int daysBetween(int y, int m, int d, int n)
{
	int s = countDay(y, m) - d;
	addOneMonth(y, m);

	while (n > 1)
	{
		if (n > 12) 
		{
			n -= 12;
			y += 1;
			s += is_leap(y) ? 366 : 365;
		}
		else 
		{
			n -= 1;
			s += countDay(y, m);
			addOneMonth(y, m);	
		}
	}
	return s + min(countDay(y, m), d);
}

void equals(int real, int expected)
{
	if (real == expected)
	{
		printf("OK\n");
	}
	else 
	{
		printf("Error\n");
	}
}

int main()
{
	// 非闰年
	equals(daysBetween(2015, 2, 1, 1), 28);
	equals(daysBetween(2015, 1, 1, 1), 31);
	// 闰年
	equals(daysBetween(2016, 1, 1, 1), 31);
	equals(daysBetween(2016, 1, 31, 1), 29);
	
	// 加多个月份的情况
	equals(daysBetween(2016, 1, 31, 2), 60);
	equals(daysBetween(2015, 1, 1, 12), 365);
	equals(daysBetween(2015, 1, 1, 12), 365);
	equals(daysBetween(2016, 1, 1, 12), 366);

	equals(daysBetween(2016, 1, 31, 12 * 5), 366 + 365 + 365 + 365 + 366);
    return 0;
}

