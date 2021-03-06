# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import socket
import sys
from paramiko.py3compat import u
from module import logger

# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False

# chan,user_obj,bind_host_obj,cmd_caches,log_recording
def interactive_shell(chan,gateway_user_obj,host_user_obj):
    if has_termios:
        posix_shell(chan,gateway_user_obj,host_user_obj)
    else:
        windows_shell(chan,gateway_user_obj,host_user_obj)


def posix_shell(chan,gateway_user_obj,host_user_obj):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        user_cmd=''
        is_tab=False
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if is_tab:
                        if x not in ('\x07' , '\r\n'):
                            user_cmd += x
                            is_tab = False
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if x!='\r':
                    user_cmd+=x
                    print("1---->",user_cmd)
                else:
                    log_msg='[%s] execute %s' %(host_user_obj.host.hostname,user_cmd)
                    logger.log_record(gateway_user_obj.id,host_user_obj.id,log_msg)

                    # add in log here
                    user_cmd=''
                if x=='\t':
                    is_tab=True
                if len(x) == 0:
                    break
                chan.send(x)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


# thanks to Mike Looijmans for this code
def windows_shell(chan,gateway_user_obj,host_user_obj):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")

    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(str(data,encoding="utf8"))
            sys.stdout.flush()

    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()

    try:
        user_cmd=''
        while True:
            d = sys.stdin.read(1)
            if d!='\n':
                user_cmd+=d
            else:
                log_msg='[%s] execute %s' %(host_user_obj.host.hostname,user_cmd)
                logger.log_record(gateway_user_obj.id,host_user_obj.id,log_msg)
                #print("3---->",user_cmd)
                # add in log here
                user_cmd=''
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass