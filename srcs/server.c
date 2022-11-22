/*****************************************************************************
 *
 *     This file is part of Purdue CS 536.
 *
 *     Purdue CS 536 is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 *
 *     Purdue CS 536 is distributed in the hope that it will be useful,
 *     but WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *     GNU General Public License for more details.
 *
 *     You should have received a copy of the GNU General Public License
 *     along with Purdue CS 536. If not, see <https://www.gnu.org/licenses/>.
 *
 *****************************************************************************/

/*
 * server.c
 * Name: Zhongtang Luo, Yu Wei
 * PUID: 32759316,
 */

#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define QUEUE_LENGTH 10000
#define RECV_BUFFER_SIZE 2048

int number_of_clients;

/* TODO: server()
 * Open socket and wait for client to connect
 * Print received message to stdout
 * Return 0 on success, non-zero on failure
 */
int server(char *server_port) {
  int sockfd, new_fd;
  struct addrinfo hints, *servinfo, *p;
  struct sockaddr_storage their_addr;
  socklen_t sin_size;
  int yes = 1;
  int recv_bytes;
  char recv_buf[RECV_BUFFER_SIZE];
  int cnt = 0;
  int rv;

  /* The address binding is inspired by Beej: https://beej.us/guide/bgnet/
   */
  memset(&hints, 0, sizeof hints);
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_flags = AI_PASSIVE;  // use my IP
  if ((rv = getaddrinfo(NULL, server_port, &hints, &servinfo)) != 0) {
    fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
    return 1;
  }
  // loop through all the results and bind to the first we can
  for (p = servinfo; p != NULL; p = p->ai_next) {
    if ((sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
      perror("server: socket");
      continue;
    }
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1) {
      perror("setsockopt");
      return 1;
    }
    if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
      close(sockfd);
      perror("server: bind");
      continue;
    }
    break;
  }
  freeaddrinfo(servinfo);  // all done with this structure
  if (p == NULL) {
    fprintf(stderr, "server: failed to bind\n");
    return 1;
  }

  if (listen(sockfd, QUEUE_LENGTH) == -1) {
    perror("listen");
    return 1;
  }

  for (; cnt < number_of_clients; ++cnt) {
    sin_size = sizeof their_addr;
    new_fd = accept(sockfd, (struct sockaddr *)&their_addr, &sin_size);
    if (new_fd == -1) {
      perror("accept");
      continue;
    }

    /* Inspired by Beej: https://beej.us/guide/bgnet/
     */
    if (!fork()) {    
      close(sockfd);  
      while ((recv_bytes = recv(new_fd, recv_buf, RECV_BUFFER_SIZE, 0)) > 0) {
        fwrite(recv_buf, 1, recv_bytes, stdout);
        fflush(stdout);
      }
      close(new_fd);
      exit(0);
    }

    close(new_fd); 
  }

  while (wait(NULL) > 0);
  return 0;
}

/*
 * main():
 * Parse command-line arguments and call server function
 */
int main(int argc, char **argv) {
  char *server_port;

  if (argc != 3) {
    fprintf(stderr, "Usage: ./server-c (server port) (number of clients)\n");
    exit(EXIT_FAILURE);
  }

  server_port = argv[1];
  number_of_clients = atoi(argv[2]);
  return server(server_port);
}
