/* C program that invokes the resetUsers script.
    Now resetFakeUsers can have root owner with setUserId
    and resetUsers can stay hidden  */

#include <stdio.h>

int main (int argc, char** args) {
  execv("/root/resetUsers", args);
}
