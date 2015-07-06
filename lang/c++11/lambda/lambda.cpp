
#include <iostream>

// Same as the functor:)
struct Add
{
	int operator()(int x, int y)
	{
		/*  ASM code from VS2012, Functor and Lambda have same ASM code.
	push	ebp
	mov		ebp, sep
	sub		esp, 0CCh
	push	ebx
	push	esi
	push	edi
	push	ecx	# Notice Here
	lea		edi, [ebp - 0CCh]
	mov		ecx, 33h
	mov		eax, 0CCCCCCCCh
	rep stos dword es:[edi]
	pop		ecx
	mov		dword ptr [this], ecx
	# +
	mov		eax, dword ptr[x]
	add		eax, dword ptr[y]
	pop		edi
	pop		esi
	pop		ebx
	mov		esp, ebp
	pop		ebp
	ret 	8
		*/
		return x + y;
	}
};

int main()
{
	auto f = [](int x, int y) {return x + y;};
	std::cout << f(2, 3) <<std::endl;
	
	return 0;
}

