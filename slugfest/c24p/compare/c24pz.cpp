// c24pz.cpp : Defines the entry point for the console application.
//
#include <stdio.h>
int A,B,C,D,N;
float r,r1,r2;
char op1,op2,op3;
char opc[4]={'+','-','*','/'};
void main() {
    N=0;
    for (A=1;A<=13;A++) {
    for (B=1;B<=13;B++) {
    for (C=1;C<=13;C++) {
    for (D=1;D<=13;D++) {
    for (op1=0;op1<4;op1++) {
    for (op2=0;op2<4;op2++) {
    for (op3=0;op3<4;op3++) {
        // ((A   @   B)  @   C)  @   D
        r=(float)A;
        switch (op1) {case 0:r =r +B ;break;case 1:r =r -B ;break;case 2:r =r *B ;break;case 3:r =r /B ;break;}
        switch (op2) {case 0:r =r +C ;break;case 1:r =r -C ;break;case 2:r =r *C ;break;case 3:r =r /C ;break;}
        switch (op3) {case 0:r =r +D ;break;case 1:r =r -D ;break;case 2:r =r *D ;break;case 3:r =r /D ;break;}
        if (23.99f<r && r<24.01f) {N++;printf("%8d: ((%2d%c%2d)%c%2d)%c%2d=24\n",N,A,opc[op1],B,opc[op2],C,opc[op3],D);}
 
        //  (A   @   B)  @  (C   @   D)
        r1=(float)A;
        switch (op1) {case 0:r1=r1+B ;break;case 1:r1=r1-B ;break;case 2:r1=r1*B ;break;case 3:r1=r1/B ;break;}
        r2=(float)C;
        switch (op3) {case 0:r2=r2+D ;break;case 1:r2=r2-D ;break;case 2:r2=r2*D ;break;case 3:r2=r2/D ;break;}
        switch (op2) {case 0:r =r1+r2;break;case 1:r =r1-r2;break;case 2:r =r1*r2;break;case 3:if (-0.01f<r2 && r2<0.01f) goto STEP3; r=r1/r2;break;}
        if (23.99f<r && r<24.01f) {N++;printf("%8d: (%2d%c%2d)%c(%2d%c%2d)=24\n",N,A,opc[op1],B,opc[op2],C,opc[op3],D);}
 
        //  (A   @  (B   @   C)) @   D
    STEP3:
        r=(float)B;
        switch (op2) {case 0:r =r +C ;break;case 1:r =r -C ;break;case 2:r =r *C ;break;case 3:r =r /C ;break;}
        switch (op1) {case 0:r =A +r ;break;case 1:r =A -r ;break;case 2:r =A *r ;break;case 3:if (-0.01f<r  && r <0.01f) goto STEP4; r=A /r ;break;}
        switch (op3) {case 0:r =r +D ;break;case 1:r =r -D ;break;case 2:r =r *D ;break;case 3:r =r /D ;break;}
        if (23.99f<r && r<24.01f) {N++;printf("%8d: (%2d%c(%2d%c%2d))%c%2d=24\n",N,A,opc[op1],B,opc[op2],C,opc[op3],D);}
 
        //   A   @ ((B   @   C)  @   D)
    STEP4:
        r=(float)B;
        switch (op2) {case 0:r =r +C ;break;case 1:r =r -C ;break;case 2:r =r *C ;break;case 3:r =r /C ;break;}
        switch (op3) {case 0:r =r +D ;break;case 1:r =r -D ;break;case 2:r =r *D ;break;case 3:r =r /D ;break;}
        switch (op1) {case 0:r =A +r ;break;case 1:r =A -r ;break;case 2:r =A *r ;break;case 3:if (-0.01f<r  && r <0.01f) goto STEP5; r=A /r ;break;}
        if (23.99f<r && r<24.01f) {N++;printf("%8d: %2d%c((%2d%c%2d)%c%2d)=24\n",N,A,opc[op1],B,opc[op2],C,opc[op3],D);}
 
        //   A   @  (B   @  (C   @   D))
    STEP5:
        r=(float)C;
        switch (op3) {case 0:r =r +D ;break;case 1:r =r -D ;break;case 2:r =r *D ;break;case 3:r =r /D ;break;}
        switch (op2) {case 0:r =B +r ;break;case 1:r =B -r ;break;case 2:r =B *r ;break;case 3:if (-0.01f<r  && r <0.01f) continue;   r=B /r ;break;}
        switch (op1) {case 0:r =A +r ;break;case 1:r =A -r ;break;case 2:r =A *r ;break;case 3:if (-0.01f<r  && r <0.01f) continue;   r=A /r ;break;}
        if (23.99f<r && r<24.01f) {N++;printf("%8d: %2d%c(%2d%c(%2d%c%2d))=24\n",N,A,opc[op1],B,opc[op2],C,opc[op3],D);}
    }
    }
    }
    }
    }
    }
    }
}