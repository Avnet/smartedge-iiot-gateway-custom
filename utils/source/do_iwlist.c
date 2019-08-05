#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <pwd.h>
#include <grp.h>
#include <string.h>
#include <shadow.h>
#include <crypt.h>

char content1[] = "{\"SSID\":\"%s\",\"SignalStrength\":\"%s\"}";

int main()
{

  FILE *fptr, *fptr1, *fptr2;
  char readbuffer[16*1024];
  char writebuffer[16*1024];
  char tempbuffer[4*1024];
  char tempbuffer1[4*1024];
  char tempbuffer2[4*1024];
  char serialnumber[32];
  while(1)
    {
  system("sudo iwlist wlan0 scan >iwlist 2>/dev/null ; cat iwlist | grep ESSID >essidlist; cat iwlist | grep Quality >signallist ;cat essidlist | cut -d ':' -f2 | tr -d '\"' >essidnames ; cat signallist | cut -d '=' -f3 >signalvalues");
 
  fptr = fopen("essidnames", "r");
  fptr1 = fopen("signalvalues", "r");
  fptr2 = fopen("/etc/WiFiAccessPointList", "w");
  //fputs("{\r\ [\r\n", fptr2);
  fwrite("[",1,1,fptr2);
  
  fgets(tempbuffer, sizeof(tempbuffer), fptr);
  fgets(tempbuffer1, sizeof(tempbuffer1), fptr1);
  while(tempbuffer[0] != 0)
    {
      tempbuffer[strlen(tempbuffer)-1] = 0;
      tempbuffer1[strlen(tempbuffer1)-1] = 0;
      sprintf(tempbuffer2, content1, tempbuffer, tempbuffer1);
      fwrite(tempbuffer2, 1, strlen(tempbuffer2), fptr2);
      memset(tempbuffer, 0, sizeof(tempbuffer));
      fgets(tempbuffer, sizeof(tempbuffer), fptr);
      fgets(tempbuffer1, sizeof(tempbuffer1), fptr1);
      if (tempbuffer[0] != 0) fwrite(",", 1, 1, fptr2);
    }
  fwrite("]", 1,1, fptr2);
  fclose(fptr);
  fclose(fptr1);
  fclose(fptr2);
  sleep(60);
    }
}
