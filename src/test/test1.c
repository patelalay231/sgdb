#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int buggy_function(int *arr, int size) {
    int sum = 0;
    for (int i = 0; i <= size; i++) {  // ⚠️ Off-by-one error (i <= size)
        sum += arr[i];  // May access out-of-bounds memory
    }
    return sum;
}

void a() {
    int *ptr = NULL;
    *ptr = 42;  
}

void buffer_overflow() {
    char buffer[5];
    strcpy(buffer, "Too long"); 
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int result = buggy_function(numbers, 5);  
    printf("Sum is: %d\n", result);

    a(); 

    buffer_overflow(); 

    return 0;
}
