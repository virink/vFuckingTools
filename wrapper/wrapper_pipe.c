#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

#define BUFSIZE 1000

char *buf;

void quit()
{
    exit(0);
}

void timeout()
{
    printf("Times Up!\n");
    fflush(stdout);
    exit(0);
}

int main(int argc, char *argv[])
{
    int p1[2];
    int p2[2];
    int pid;

    buf = (char*) malloc(BUFSIZE);
    int n;

    if( argc < 2 ){
        fprintf(stderr, "There is no argv\n");
        exit(0);
    }

    char exe[50];
    sprintf(exe,"./%s",argv[1]);

    fprintf(stdout, "pwn: %s\n",exe);

    pipe(p1);
    pipe(p2);
    pid = fork();

    if (pid){ //parent
        signal(SIGCHLD, quit);
        signal(SIGALRM, timeout);
        alarm(10);

        close(p1[0]);
        close(p2[1]);

        // get
        n = read(p2[0], buf, BUFSIZE);
        write(1, buf, n);

        while (1) {
            // hijack input
            n = read(0, buf, BUFSIZE);
            if (strstr(buf, "flag")) { // filter
                fprintf(stderr, "pwn?\n");
                exit(0);
            }

            write(p1[1], buf, n);
            bzero(buf, BUFSIZE);

            // hijack output
            n = read(p2[0], buf, BUFSIZE);
            write(1, buf, n);
        }

    } else { //child
        close(p1[1]);
        close(p2[0]);
        dup2(p1[0], 0);
        dup2(p2[1], 1);
        execve(exe, NULL, NULL);
    }

    return 0;
}
