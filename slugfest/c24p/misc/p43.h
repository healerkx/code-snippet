
/**
 * Calc P-4-3, 64 status.
 *
 */
class P43
{
public:
	P43() : _i(0) { }

	inline bool move(int& a, int& b, int& c)
	{
		if (_i < 64)
		{
			a = (_i & 0x30) >> 4;
			b = (_i & 0x0C) >> 2;
			c = _i & 0x03;
			++_i;
			return true;
		}
		return false;
	}
private:
	int	_i;
};