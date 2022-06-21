# include <stdio.h>
# include <stdlib.h>

int main (int argc, char** argv) {
  char c;
  FILE* inFile;
  FILE* outFile;
  char outFileName[256];
  if (argc != 3) {
    printf("program usage: ./copy <infile> <outfile>\n");
    exit(1);
  }
  snprintf(outFileName, sizeof(outFileName), "%s/%s", getenv("HOME"), argv[2]);
  inFile = fopen(argv[1], "r");
  outFile = fopen(outFileName, "w");
  printf("Copying %s to %s\n", argv[1], outFileName);
  while ((c = fgetc(inFile)) != EOF) {
	fprintf(outFile, "%c", c);
  }
  fclose(inFile);
  fclose(outFile);
}
