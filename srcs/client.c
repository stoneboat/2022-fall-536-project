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
 * client.c
 * Name: Zhongtang Luo, Yu Wei
 * PUID: 32759316, 
 */

#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define SEND_BUFFER_SIZE 2048

/* TODO: client()
 * Open socket and send message from stdin.
 * Return 0 on success, non-zero on failure
 */
int client(char *server_ip, char *server_port) {
  int sockfd, numbytes, sentbytes;
  char buf[SEND_BUFFER_SIZE], *buf_p;
  struct addrinfo hints, *servinfo, *p;
  int rv;

  /* The address binding is inspired by Beej: https://beej.us/guide/bgnet/
   */
  memset(&hints, 0, sizeof hints);
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  if ((rv = getaddrinfo(server_ip, server_port, &hints, &servinfo)) != 0) {
    fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
    return 1;
  }
  for (p = servinfo; p != NULL; p = p->ai_next) {
    if ((sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
      perror("client: socket");
      continue;
    }
    if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
      close(sockfd);
      perror("client: connect");
      continue;
    }
    break;
  }
  if (p == NULL) {
    fprintf(stderr, "client: failed to connect\n");
    return 2;
  }
  freeaddrinfo(servinfo);  // all done with this structure

  while (numbytes = fread(buf, 1, SEND_BUFFER_SIZE, stdin)) {
    buf_p = buf;
    while (buf_p < buf + numbytes) {
      if ((sentbytes = send(sockfd, buf_p, buf + numbytes - buf_p, 0)) == -1) {
        perror("send");
        return 1;
      }
      buf_p += sentbytes;
    }
  }
  close(sockfd);

  return 0;
}

/*
 * main()
 * Parse command-line arguments and call client function
 */
int main(int argc, char **argv) {
  char *server_ip;
  char *server_port;

  if (argc != 3) {
    fprintf(stderr,
            "Usage: ./client-c (server IP) (server port) < (message)\n");
    exit(EXIT_FAILURE);
  }

  server_ip = argv[1];
  server_port = argv[2];
  return client(server_ip, server_port);
}
