
#include <stdio.h>
#include <string.h>
#pragma warning(disable: 4996)

char res[0xff * 8] = { 0 };
#define IF_ENTER_RETURN(x, y) if (x == '\n' || x == '\r') return y;

int getlength(char* s, int& len)
{
    len = 0;
    IF_ENTER_RETURN((*s), 1);
    char* p = s;
    int b = 0;
    int a = 0;
    bool bFind = false;
    while (*p)
    {
        if ((b == 15 || b == 16) && !bFind)
        {
            len = 0;
            return b;
        }

        if (*p == '_' && *(p + 1) == '/')
        {
            bFind = true;
            a += 1;
            b += 2;
            if (a >= 3)
                break;
            p = p + 2;
        }
        else if (*p == ' ')
        {
            if (bFind)
            {
                break;
            }
            b++;
            p = p + 1;
        }
        else if (*p == '\r' || *p == '\n')
        {
            break;
        }
        else if (*p == '*')
        {
            break;
        }
    }
    len = a;
    return b;
}


void parse_file(const char* filename)
{
    FILE* fp = fopen(filename, "r");
    if (fp == NULL)
        return;
    char ln[0xff * 8] = { 0 };
    char ch = 0;
    int a = 0;
    fread(ln, 0xff*8, 1, fp);
    a = strlen(ln);
    int temp = 0;
    int count = 0;
    int r = 0;
    while (temp <= a)
    {
        int c = 0;
        char* p = ln + temp;
        int len = getlength(p, c);
        if (len == 1 && c == 0)
        {
            res[count] = '#';
            len = 2;
            temp += 1;
            count++;

        }
        else if ((len == 16 || len == 15) && c == 0)
        {
            res[count] = (len + 8) * 4 + (3 - c);
            temp += len;
            count++;
        }
        else if (len > 0 && c > 0)
        {
            res[count] = (len + 8) * 4 + (3 - c);
            temp += len;
            count++;
        }
        else if (len == 0 && c == 0)
        {
            break;
        }

    }
	printf("%s\n", res);
}

int main(int a)
{
	parse_file(".\\name.txt");
	char* x = res;	//"bB_Z#^B_Z#h1AI.BMB5#VB2>2:B>>=6#RB@1.>>L12#NB6N:>BN#JFHL1@D6#";
    while(a = *x / 4) a -= 8, printf("\n%*s" + !!a, a, "_/_/_/" + *x++ % 4 * 2);
	return 0;
}