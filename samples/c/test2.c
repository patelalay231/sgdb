#include <stdio.h>
#include <limits.h>

/*
 * adapted from http://blog.regehr.org/archives/213
 *
 * Try compiling this with -O0 and with -O3, and see ...
 */
void compare (unsigned int a) {
	if ((a+1) > a)
		printf("%u > %u\n", (a+1), a);
	else
		printf("%u <= %u\n", (a+1), a);
}

int main () {
	compare(1);
	compare(INT_MAX);
}