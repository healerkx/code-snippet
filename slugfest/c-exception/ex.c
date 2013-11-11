
#include <setjmp.h>
#include <stdio.h>
#include <malloc.h>

#pragma warning(disable:4996)

#define EXCEPTIOND	jmp_buf __JMP_BUF__
#define EXCEPTION	__JMP_BUF__
#define TRY			EXCEPTIOND; if (!setjmp(EXCEPTION))
#define CATCH		else
#define THROW		longjmp(EXCEPTION, 0)

int read_files(FILE* f, char* buffer, int size, EXCEPTIOND)
{
	size_t r = fread(buffer, 1, size, f);
	buffer[r] = '\0';
	return r;
}

int write_files(FILE* f, char* buffer, int size, EXCEPTIOND)
{
	THROW;	// Assume throws exception when write the file.
	return 0;
}

int files_work()
{
	FILE* f1 = 0;
	FILE* f2 = 0;
	char* buffer = 0;
	int s = 1024;
	int r = 0;
	TRY
	{
		f1 = fopen("./file_to_read", "r");
		if (!f1) 
			THROW;
		f2 = fopen("file_to_write", "w");
		if (!f2) 
			THROW;
		
		buffer = (char*)malloc(s);
		r = read_files(f1, buffer, s, EXCEPTION);
		if (r > 0)
		{
			write_files(f2, buffer, r, EXCEPTION);
		}
		THROW;
	}
	CATCH
	{
		if (f1) 
			fclose(f1);

		if (f2)
			fclose(f2);

		if (buffer)
			free(buffer);
	}

	return 0;
}





int main()
{
	files_work();
	return 0;
}