/*-
 * Copyright (c) 2005,2006 Peter Wemm
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * $Id: w800rf32.c,v 1.3 2005/12/13 07:56:22 peter Exp $
 */

#include <sys/types.h>
#include <sys/time.h>
#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdarg.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <time.h>
#include <unistd.h>

#if defined(__FreeBSD__) || defined(HAVE_ERR)
#include <err.h>
#else
static void
boom(int ex, const char *fmt, ...)
{
	va_list ap;

	va_start(ap, fmt);
	vprintf(fmt, ap);
	printf(": %s\n", strerror(errno));
	va_end(ap);
	exit(ex);
}
#define err boom
#endif
volatile int timeout;

void
sigalarm(int sig)
{
	timeout = 1;
}

int
main(int ac, char *av[])
{
	struct sigaction sa;
	struct termios tio;
	struct timeval tv, tv1;
	int lastuc[16];
	char raw2hc[16] = "MNOPCDABEFGHKLIJ";
	char rcvd[16];
	char rcvd1[16];
	char syscmd[80];
	uint8_t c[4];
	int fd;
	int n, fl, i;
	int hc;
	int uc;
	int state;
	int ch;
	int debug;
	int timelimit;
	time_t t;
	FILE *log;
	char *dev;
	char *logfile;
	char *pidfile;
	char *cmd;

	timelimit = 2;
	dev = "/dev/ttyd5";
	logfile = "/usr/local/x10/w800rf32.log";
	pidfile = "/var/run/w800rf32.pid";
	cmd = "/usr/local/x10/x10rf.sh";
	debug = 0;
	while ((ch = getopt(ac, av, "c:Dd:l:p:t:")) != -1) {
		switch (ch) {
		case 'c':
			cmd = optarg;
			break;
		case 'D':
			debug++;
			break;
		case 'd':
			dev = optarg;
			break;
		case 'l':
			logfile = optarg;
			break;
		case 'p':
			pidfile = optarg;
			break;
		case 't':
			timelimit = atoi(optarg);
			if (timelimit > 0)
				break;
			fprintf(stderr, "timelimit must be positive in seconds\n");
			/* Fall through */
		case '?':
			fprintf(stderr, "usage: %s [-D] [-d device] [-l logfile] [-p pidfile] [-t timelimit]\n", av[0]);
			exit(1);
		}
	}
	fd = open(dev, O_RDWR | O_NDELAY);
	if (fd < 0)
		err(1, "open(%s) failed", dev);
	tcgetattr(fd, &tio);
	cfmakeraw(&tio);
	cfsetspeed(&tio, 4800);
	tio.c_cflag |= CLOCAL;
	tcsetattr(fd, TCSADRAIN, &tio);
	tcflush(fd, TCIOFLUSH);
	/* eat any queued characters */
	while ((n = read(fd, &c[0], 1)) == 1) {
		/* nothing */ ;
	}
	fl = fcntl(fd, F_GETFL);
	fl &= ~O_NONBLOCK;
	fcntl(fd, F_SETFL, fl);
	memset(&sa, 0, sizeof(sa));
	sigemptyset(&sa.sa_mask);
	sa.sa_flags = 0;	/* NO SA_RESTART */
	sa.sa_handler = sigalarm;
	n = sigaction(SIGALRM, &sa, NULL);
	if (n == -1)
		err(1, "sigaction(SIGALARM) failed");
	if (!debug) {
		/* Fork and detach */
#if defined(__FreeBSD__) || defined(HAVE_DAEMON)
		daemon(0, 0);
#else
		pid_t pid;

		pid = fork();
		switch (pid) {
		case 0:
			setsid();
			close(0);
			close(1);
			close(2);
			open("/dev/null", O_RDONLY);
			open("/dev/null", O_WRONLY);
			open("/dev/null", O_WRONLY);
			chdir("/");
			break;
		case -1:
			err(1, "fork failed");
		default:
			_exit(0);
		}
#endif
	}
	log = fopen(pidfile, "w");
	if (log) {
		fprintf(log, "%d", getpid());
		fclose(log);
	}
	log = fopen(logfile, "a");

	state = 0;
	for (;;) {
restart:
		timeout = 0;
		for (i = 0; timeout == 0 && i < 4; i++) {
			n = read(fd, &c[i], 1);
			if (n == 1)
				alarm(2);
			if (n == -1 && errno == EINTR) {
				printf("out of sync, resyncing\n");
				goto restart;
			}
			if (n == -1) {
				perror("read error");
				goto restart;
			}
		}
		alarm(0);

		if ((c[0] & 0xf0) == (c[1] & 0xf0) && c[2] == (~c[3] & 0xff) &&
		    (c[0] & 0x0f) == (~c[1] & 0x0f)) {
			if (c[2] == 0)
				snprintf(rcvd, sizeof(rcvd), "S%02X OPEN", c[0]);
			else
				snprintf(rcvd, sizeof(rcvd), "S%02X CLOSE", c[0]);
		} else if (c[0] == (~c[1] & 0xff) && c[2] == (~c[3] & 0xff)) {
			hc = (c[0] >> 4) & 15;
			if (c[2] & 0x80) {
				uc = lastuc[hc];
				if (c[2] & 0x10)
					snprintf(rcvd, sizeof(rcvd), "%c%02d DIM", raw2hc[hc], uc);
				else
					snprintf(rcvd, sizeof(rcvd), "%c%02d BRIGHT", raw2hc[hc], uc);
			} else {
				uc = ((c[2] & 0x10) >> 4) |
				     ((c[2] & 0x8) >> 2)  |
				     ((c[2] & 0x40) >> 4) |
				     ((c[0] & 0x04) << 1);
				uc += 1;
				lastuc[hc] = uc;
				if (c[2] & 0x20)
					snprintf(rcvd, sizeof(rcvd), "%c%02d OFF", raw2hc[hc], uc);
				else
					snprintf(rcvd, sizeof(rcvd), "%c%02d ON", raw2hc[hc], uc);
			}
		} else {
			snprintf(rcvd, sizeof(rcvd), "X%02x%02x%02x%02x", c[0], c[1], c[2], c[3]);
		}
		if (state == 1) {
			if (strcmp(rcvd, rcvd1) != 0) {
				/* Different, process it anyway */
				state = 0;
				/* fall through to next case */
			} else {
				gettimeofday(&tv, NULL);
				tv.tv_sec -= tv1.tv_sec;
				tv.tv_usec -= tv1.tv_usec;
				if (tv.tv_usec < 0) {
					tv.tv_sec--;
					tv.tv_usec += 1000000;
				}
				if (tv.tv_sec >= timelimit) {
					/* Timeout, process it anyway */
					state = 0;
					/* fall through to next case */
				}
			}
		}
		if (state == 0) {
			if (log) {
				t = time(0);
				fprintf(log, "%-10s %s", rcvd, ctime(&t));
				fflush(log);
				if (debug)
					printf("%s\n", rcvd);
			}
			snprintf(syscmd, sizeof(syscmd), "%s %s &", cmd, rcvd);
			system(syscmd);
			strcpy(rcvd1, rcvd);
			gettimeofday(&tv1, NULL);
			state = 1;
		}
	}
}
