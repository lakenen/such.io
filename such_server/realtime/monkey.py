import sys
import socket
from redis._compat import BytesIO
from redis.exceptions import ConnectionError

def read(self, length=None):
    """
    Read a line from the socket if no length is specified,
    otherwise read ``length`` bytes. Always strip away the newlines.
    """
    try:
        if length is not None:
            bytes_left = length + 2  # read the line ending
            if length > self.MAX_READ_LENGTH:
                # apparently reading more than 1MB or so from a windows
                # socket can cause MemoryErrors. See:
                # https://github.com/andymccurdy/redis-py/issues/205
                # read smaller chunks at a time to work around this
                try:
                    buf = BytesIO()
                    while bytes_left > 0:
                        read_len = min(bytes_left, self.MAX_READ_LENGTH)
                        buf.write(self._fp.read(read_len))
                        bytes_left -= read_len
                    buf.seek(0)
                    return buf.read(length)
                finally:
                    buf.close()
            return self._fp.read(bytes_left)[:-2]

        # no length, read a full line

        # readline is buffered, so #badnewsbears
        #return self._fp.readline()[:-2]

        # let's do it totally unbuffered instead!
        buf = BytesIO()
        byte = None
        while byte != '\n':
            byte = self._fp.read(1)
            buf.write(byte)
        buf.seek(0)
        return buf.read()[:-2]
    except (socket.error, socket.timeout):
        e = sys.exc_info()[1]
        raise ConnectionError("Error while reading from socket: %s" %
                              (e.args,))
