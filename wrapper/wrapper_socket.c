#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>

#define BUFSIZE 1000
#define SOCK_PATH "/tmp/wrapper"

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

int main()
{

    int pid;

    buf = (char*) malloc(BUFSIZE);
    int n;

    unlink(SOCK_PATH);
    int s = socket(AF_UNIX, SOCK_STREAM, 0);
    struct sockaddr_un addr;
    memcpy(addr.sun_path, SOCK_PATH, strlen(SOCK_PATH));
    addr.sun_family = AF_UNIX;
    bind(s, (struct sockaddr *)&addr, strlen(addr.sun_path) + sizeof(addr.sun_family));
    listen(s, 5);

    pid = fork();

    if (pid){ //parent
        signal(SIGCHLD, quit);
        signal(SIGALRM, timeout);
        alarm(10);

        struct sockaddr_un child;
        int clen = sizeof(child);
        int cs = accept(s, (struct sockaddr *) &child, &clen);

        if (cs == -1) {
            fprintf(stderr, "server socket fail\n");
            exit(0);
        }

        // get
        n = read(cs, buf, BUFSIZE);
        write(1, buf, n);

        while (1) {
            // hijack input
            n = read(0, buf, BUFSIZE);
            if (strstr(buf, "flag")) { // filter
                fprintf(stderr, "pwn?\n");
                exit(0);
            }

            write(cs, buf, n);
            bzero(buf, BUFSIZE);

            // hijack output
            n = read(cs, buf, BUFSIZE);
            write(1, buf, n);
        }

    } else { //child
        int s = socket(AF_UNIX, SOCK_STREAM, 0);
        struct sockaddr_un addr;
        bzero(addr.sun_path, sizeof(addr.sun_path));
        memcpy(addr.sun_path, SOCK_PATH, strlen(SOCK_PATH));
        addr.sun_family = AF_UNIX;
        connect(s, (struct sockaddr *)&addr, strlen(addr.sun_path) + sizeof(addr.sun_family));
        if (s == -1) {
            fprintf(stderr, "cli socket fail\n");
            exit(0);
        }
        dup2(s, 0);
        dup2(s, 1);
        execve("./applestore", NULL, NULL);
    }

    return 0;
}
