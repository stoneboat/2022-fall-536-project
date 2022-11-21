all: client server

.phony: all test

client: client.c
	gcc client.c -o client

server: server.c
	gcc server.c -o server

test: all
	python3 test.py

clean:
	rm client server