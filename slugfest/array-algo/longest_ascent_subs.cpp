int longest_ascent_sequence(int* p, int n)
{
	int *o = new int[n];
	for (int i = 0; i < n; ++i)
	{
		o[i] = 1;
	}

	for (int i = 1; i < n; ++i)
	{
		int max = 0;
		for (int j = 0; j < i; j++)
		{
			if (p[i] > p[j])
			{
				if (max < o[j])
				{
					max = o[j];
				}
			}
			o[i] = max + 1;
		}

	}

	int r = 0;
	for (int i = 0; i < n; ++i)
	{
		if (r < o[i]) r = o[i];
	}
	
	return r;

}
