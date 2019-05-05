default:
	@echo "\tmake hookall"
	@echo "\tmake hook64"
	@echo "\tmake hook32"
	@echo "\tmake pipe"
	@echo "\tmake socket"

hookall: hook64 hook32

hook64: hook.c mdir
	gcc -fPIC -shared -o bin/hook.so hook.c -ldl
hook32: hook.c mdir
	gcc -m32 -fPIC -shared -o hook.so.32 hook.c -ldl
pipe: mdir
	gcc wrapper_pipe.c -o bin/wrapper_pipe
socket: mdir
	gcc wrapper_socket.c -o wrapper_socket
mdir:
	mkdir bin