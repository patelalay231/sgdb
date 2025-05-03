#include <iostream>

using namespace std;

struct B {
  virtual void whoami ()
    {cout << "B" << endl;}
};

struct D : public B {
  void whoami ()
    {cout << "D" << endl;}
};

int main() {
  D d;
  B *b = &d;
  b->whoami();
  D *dd = &d;
  dd->whoami();
}