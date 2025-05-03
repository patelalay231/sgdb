#include <iostream>

using namespace std;

int * f(int x) {
  return &x;
}

int * g(int x, int y) {
  return &y;
}

int * h(int x, int y, int z) {
  return &z;
}

int main() {
  cout << *f(42) << endl;
  int * y1 = g(43, 44);
  int * y2 = g(45, 46);
  cout << *y1 << ", " << *y2 << endl;
  int * z1 = h(47, 48, 49);
  int * z2 = h(50, 51, 52);
  cout << *z1 << ", " << *z2 << endl;
  return 0;
}