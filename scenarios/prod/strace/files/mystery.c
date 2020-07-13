#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>

/* 
 * mystery <filename> <string>
 * Appends <string> (with newline) to the end of /tmp/<filename> 
 * and sets permissions of /tmp/<filename> to 754
 */
int main (int argc, char** argv) {
  char tmpFilename[1024];
  int tmpFileFd;
  char* filename = argv[1];  
  char* string = argv[2];
  snprintf(tmpFilename, sizeof(tmpFilename), "/tmp/%s", filename);
  tmpFileFd = open(tmpFilename, O_CREAT|O_WRONLY|O_APPEND); 
  write(tmpFileFd, string, strlen(string));
  write(tmpFileFd, "\n", 1);
  fchmod(tmpFileFd, S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IXGRP|S_IROTH);
  // The above is equivalent to fchmod(tmpFileFd, 0754)
  close(tmpFileFd);
}
