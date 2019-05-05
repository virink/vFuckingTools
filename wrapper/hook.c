#include <dlfcn.h>

void free(void *ptr)
{
    void *lib = dlopen("/lib/x86_64-linux-gnu/libc.so.6", RTLD_LAZY);
    void (*_free)();

    _free = (void(*)()) dlsym(lib, "free");
    dlclose(lib);

    _free(ptr);

}

int puts(const char *s)
{
    void *lib = dlopen("/lib/x86_64-linux-gnu/libc.so.6", RTLD_LAZY);
    int (*_puts)(const char*);

    _puts = (int(*)()) dlsym(lib, "puts");
    dlclose(lib);
    return _puts(s);
}
