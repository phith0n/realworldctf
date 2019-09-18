#include <stdio.h>

int main () {
   FILE *fp;
   char buff[255];

   fp = fopen("/flag", "r");
   fgets(buff, 255, fp);
   fclose(fp);

   printf("flag: %s\n", buff);

   return 0;
}