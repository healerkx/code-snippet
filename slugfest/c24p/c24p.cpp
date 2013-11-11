// c24p.cpp : Defines the entry point for the console application.
//
#pragma warning(disable: 4996)
#include <stdio.h>
#include "misc\p43.h"
#include <cassert>
#include <math.h>
#include <vector>
#include <functional>
#include <string>

#define UNACCEPT				-1

#define EPSINON					0.0001
#define FEQU(x, y)				((x - y) >= -EPSINON && (x - y) <= EPSINON)
#define FZERO(x)				((x) >= -EPSINON && (x) <= EPSINON)
#define VALIDR(x, y, z)			(FEQU(x, (int)x) && x >= y && x <= z)
#define	LP(x)					(x == 0 || x == 1)
#define HP(x)					(x == 2 || x == 3)
#define CE(x)					(x == 0 || x == 2)
#define	ALL_PM(x, y, z)			(LP(x) && LP(y) && LP(z))
#define	ALL_MD(x, y, z)			(HP(x) && HP(y) && HP(z))
#define	BTH_PM(x, y)			(LP(x) && LP(y))
#define	BTH_MD(x, y)			(HP(x) && HP(y))
#define SAMEPRIO(x, y)			(BTH_PM(x, y) || BTH_MD(x, y))
#define ASCENDING(x, y, z)		(z >= y && y >= x)
#define STR3FIND(x, s)			(x[0] == s ? 0 : (x[1] == s ? 1 : 2))

enum ExpType
{
	unknown = -2,
	number = -1,
	plus = 0,
	minus = 1,
	multi = 2,
	divi = 3
};


class expr
{
public:
	expr()
		:_left(0), _right(0), _type(unknown), _calculated(0)
	{
	}

	
	inline void left(expr* n) { _left = n; }
	inline void right(expr* n) { _right = n; }
	
	inline expr* left() const { return _left; }
	inline expr* right() const { return _right; }

	inline ExpType type() const { return _type; }
	inline void type(int type) { _type = (ExpType)type; }

	inline double value() const { return _result; }
	inline void value(double n)
	{
		_result = n;
		_type = number;
	}

	bool calc(double& result)
	{
		if (!_left || !_right)
			return false;

		double lv, rv;
		if (_left->type() == number)
			lv = _left->value();
		else if(!_left->calc(lv))
			return false;

		if (_right->type() == number)
			rv = _right->value();
		else if(!_right->calc(rv))
			return false;


		switch (_type)
		{
		case 0:	return (result = lv + rv), true;
		case 1:	return (result = lv - rv), true;
		case 2:	return (result = lv * rv), true;
		case 3:	
			{
				return (FEQU(rv, 0.0)) ? false : ((result = lv / rv), true);
			}
		default:
			return false;
		}
		return 0.0;
	}

	// Inverse operation
	friend bool calc_to(expr* root, expr* x, double result);
private:
	ExpType	_type;
	int		_calculated;
	double	_result;
	expr*	_left;
	expr*	_right;
};

bool calc_to(expr* e, expr* x, double result)
{
	if (e->type() == number)
		return (x->value(result)), true;

	if (!e->left() || !e->right())
		return false;

	double p;
	if (e->left()->type() == number)
	{
		expr* right = e->right();
		if (right == x)
			p = e->left()->value();
		else if (!right->calc(p))
			return false;

		switch (e->type())
		{
		case 0:	
			return x->value(result - p), true;
		case 1:	
			return x->value(result + p), true;
		case 2:	
			return FEQU(p, 0.0) ? false : x->value(result / p), true;
		case 3:	
			return FEQU(p, 0.0) ? false : x->value(result * p), true;
		default:
			return false;
		}
	}
	else if (e->right()->type() == number)
	{
		expr* left = e->left();
		if (!left->calc(p))
			return false;
		switch (e->type())
		{
		case 0:	
			return x->value(result - p), true;
		case 1:
			return x->value(p - result), true;
		case 2:	
			return FEQU(p, 0.0) ? false : x->value(result / p), true;
		case 3:	
			return FEQU(result, 0.0) ? false : x->value(p / result), true;
		default:
			return false;
		}
	}
	else
	{
		if (!e->left()->calc(p))
			return false;
		switch (e->type())
		{
		case 0:	
			return calc_to(e->right(), x, result - p);
		case 1:
			return calc_to(e->right(), x, p- result);
		case 2:
			return FEQU(p, 0.0) ? false : calc_to(e->right(), x, result / p);
		case 3:
			return calc_to(e->right(), x, p / result);
		default:
			return false;
		}
	}

}

class context_loop
{
public:
	context_loop()
		:_starts(1), _ends(13), _l(4), _f(3), _flag(0)
	{
		for (int i = 0; i < _l; ++i)
		{
			_c[i] = 1;
		}
		_c[3] = 0;
	}

	void init(const char* p)
	{
		int p1 = _p1 = STR3FIND(p, '1');
		int p2 = _p2 = STR3FIND(p, '2');
		int p3 = _p3 = STR3FIND(p, '3');
		_n[0].type(number);
		_n[1].type(number);
		_n[2].type(number);
		_n[3].type(number);
		_e3.left(&_n[p3]);
		_e3.right(&_n[p3 + 1]);
		if (p1 == 1) // 213, No 312
		{
			_e2.left(&_n[0]);	
			_e2.right(&_n[1]);

			_e1.left(&_e2);
			_e1.right(&_e3);
		}
		else
		{
			if (p2 < p3)
			{
				_e2.right(&_e3);
				_e2.left(&_n[p2]);
			}
			else
			{
				_e2.left(&_e3);
				_e2.right(&_n[p2 + 1]);
			}

			if (p1 < p2)
			{
				_e1.left(&_n[p1]);
				_e1.right(&_e2);
			}
			else
			{
				_e1.right(&_n[p1 + 1]);
				_e1.left(&_e2);
			}
		}
		_s[0] = _s[1] = _s[2] = _s[3] = &_starts;
	}

	void settypes(int (&o)[3])
	{
		_e1.type(o[_p1]);
		_e2.type(o[_p2]);
		_e3.type(o[_p3]);

	}

	void set_ends(int ends)
	{
		_ends = ends;
	}

	void starts_base_on(int c, int p, bool clear = false)
	{
		if (clear)
		{
			_s[c] = &_starts;
			return;
		}
		_s[c] = &_c[p];
	}

	void constraints(int flag)
	{
		_flag = flag;
	}

	bool move()
	{
		while (true)
		{
			if (_c[_f] + 1 <= _ends)
			{
				_c[_f] += 1;
				while (_f < _l - 1)
				{
					if (_s[_f + 1] != &_starts)
					{
						_c[_f + 1] = *_s[_f + 1];
					}
					_f++;
				}
				if (_flag != 0)
				{
					if (_c[0] == _c[2] && _c[1] > _c[3])
					{
						continue;
					}
				}

				return true;
			}
			else
			{
				_c[_f] = *_s[_f];
				if (_f > 0)
					_f--;
				else
					return false;
			}
		}
	}

	bool calc(double& result)
	{
		_n[0].value(_c[0]);
		_n[1].value(_c[1]);
		_n[2].value(_c[2]);
		_n[3].value(_c[3]);
		return _e1.calc(result);
	}

	int operator[](int i) const
	{
		return _c[i];
	}
private:
	int		_flag;
	int		_starts;
	int		_ends;
	int		_p1;
	int		_p2;
	int		_p3;
	int		_l;
	int		_f;
	int		_c[4];
	int*	_s[4];
	expr	_n[4];
	expr	_e1;
	expr	_e2;
	expr	_e3;
};

static int count = 0;
FILE* f;

bool calc(const char* p, context_loop& cl, int (&o)[3])
{
	double r = 0.0;
	cl.settypes(o);
	while (cl.move())
	{
		if (cl[0] == 12&& cl[1] == 12&&cl[2] == 7&& cl[3] == 7 &&  o[1]==3 && o[0] ==0 && o[2]==1)
		{
			int aa = 0;
		}
		if (cl.calc(r))
		{
			if (FEQU(r, 24.0))
			{
				char buffer[1024] = {};
				
				int c = sprintf_s(buffer, 1024, "%s %d %d %d  %d %d %d %d\n", p, o[0], o[1], o[2], cl[0], cl[1], cl[2], cl[3]);
				buffer[c] = 0;
				fwrite(buffer, c, 1, f);
				printf(buffer);
				count++;
			}
		}
	}

	return false;

}

bool check(const char* p, int (&o)[3], context_loop& cl)
{
	int p1 = STR3FIND(p, '1');
	int p2 = STR3FIND(p, '2');
	int p3 = STR3FIND(p, '3');
	if (SAMEPRIO(o[p2], o[p3]))  // 2 3 same priority, 1 not.
	{
		//return false;
		if (p1 == 1)  // p1 ==1	//213
		{
			if (CE(o[1]) && (o[0] > o[2]))  // 2/3 + 2*3 NotOK
			{
				return false;
			}
			// TODO:

			if (CE(o[0]))
			{
				cl.starts_base_on(1, 0);
			}
			if (CE(o[2]))
			{
				cl.starts_base_on(3, 2);
			}
			// TODO: Bug!!!!
			if (CE(o[1]) && o[0] == o[2])
			{
				cl.starts_base_on(2, 0);
				cl.constraints(1);
				
			}
			
			return true;
		}
		else
		{
			// 123 132 231 321 (p2>p3)=>  132 321
			if (p3 < p2)  // 132 #321
			{
				if (p1 == 2 && CE(o[2]))
				{
					return false; // 231 But 1 is +*;  (a+b+c) * d  <=> d * (a+b+c)
				}
				// TODO: a*(b@c@d)  (a@b@c) / d
				if (o[p3] <= o[p2])
				{
					
					if (CE(o[p3]) && CE(o[p2]))	//**
					{
						cl.starts_base_on(p3 + 1, p3);
						cl.starts_base_on(p2 + 1, p2);
					}
					else if (CE(o[p3]))	// */
					{
						cl.starts_base_on(p3 + 1, p3);
					}
					else // //
					{
						cl.starts_base_on(p2 + 1, p2);
					}
					return true;
				}
			}
		}
	}
	//////////////////////////////////////////////////////////
	else if (SAMEPRIO(o[p1], o[p2]))
	{
		if (p3 == 0)
		{
			// E/a/b
			if (o[1] == o[2] && !CE(o[1]))
			{
				if (CE(o[0]))
				{
					cl.starts_base_on(1, 0);
				}
				cl.starts_base_on(3, 2);
				return true; // E/a/b   E-a-b
			}
		}
		else if (p3 == 2) // a@b@(c#d)
		{
			if (o[0] > o[1])
			{
				return false;
			}
			if (p1 > p2)
			{
				return false;
			}
			if (CE(o[0]))
			{
				cl.starts_base_on(1, 0);
			}
			if (CE(o[2]))
			{
				cl.starts_base_on(3, 2);
			}
			return true;
		}
		return false;

	}
	else ////////////////////////////////////////////////////////////
	{
		
		//assert(SAMEPRIO(o[p1], o[p3]));	// a + (b * (c - d)) 123     a*b + (c+d)  213
		if (p1 == 1) //a*b + (c+d) => 213, No 312
		{
			// (a+b) * (c * d) <=>  E * c *d    FOR SAMEPRIO(o[p1], o[p2])
			return false;
		}
		else // 1 NoMiddle, 123 132 231 321
		{
			if (p1 == 2 && CE(o[2]))// 1 at last but is *+
			{
				return false;
			}
			// a + (b * c+d)), a+((c+d)*b), ((c*d)-b)/a
			if (CE(o[p2]) && (p2 > p3))
			{
				return false;
			}

			// Only C&D need to ... 
			if (CE(o[p3]))
			{
				cl.starts_base_on(p3 + 1, p3);
			}
			return true;
		}
	}
	return false;
}

void f1()
{
	const char* p[] = { "123", "132", "213", "231", "321"};
	int acceptState = -1;

	

	P43 oploop;
	int o[3];
	int c2 = 0;
	while (oploop.move(o[0], o[1], o[2]))
	{
		if (ALL_PM(o[0], o[1], o[2]) || ALL_MD(o[0], o[1], o[2]))
		{
			if (ASCENDING(o[0], o[1], o[2]))	//301
			{
				if (o[0] == o[1] && o[2] == 2)
				{
					int aa = 0;
				}
				context_loop cl;
				cl.init(p[4]);
				cl.settypes(o);

				bool ch = false;
				int last = o[0];
				bool clear = !CE(o[0]);
				if (CE(o[0]))
				{
					cl.starts_base_on(1, 0, clear);
				}
				for (int i = 1; i < 3; ++i)
				{
					if (o[i] == o[i - 1])
					{
						cl.starts_base_on(i + 1, i);
					}
					else
					{
						cl.starts_base_on(i + 1, i, true);
					}
				}

				calc(p[4], cl, o);

				continue;
			}

		}
		else
		{
			//---
			for (int i = 0; i < 5; ++i)
			{
				if (i != 3 && i != 4)
				{
					//continue;
				}
				context_loop cl;
				cl.init(p[i]);
				cl.settypes(o);

				if (check(p[i], o, cl))
				{
					calc(p[i], cl, o);
				}
				else
				{
					//count2++;
				}
			}

		}
	}

}

int main(int argc, wchar_t* argv[])
{

	f = fopen("logs.txt", "w");
	f1();
	fclose(f);
	printf("%d\n", count);
	return 0;
}