import socket
import string

from .exceptions import SrcpError, ProtocolError
from .logger import log


class SrcpConnection:
    """
    Handle the connection to the SRCP server.
    """

    def __init__(self):
        self._commandsockets = []
        self._commandsocketsf = []
        self._locos = {}
        self._accessories = {}
        self._InfoportS = None
        self._InfoportF = None
        self._PollportS = None
        self._fb_procs = {}
        self._ga_procs = []
        self._timeoutproc = [0, None]
        self._inputProc = (None, None)
        self.host = None
        self.port = None

    def connect(self, host: str = 'localhost', port: int = 4303) -> str:
        """Establish a new connection to the SRCP-server

        host and port specifiy the parameters of how to connect the server.
        If the connection could not be established the according exception
        will be raised.

        """
        socket_index = len(self._commandsockets)
        self._commandsockets.append(
            socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        )
        self.host = host
        self.port = port
        try:
            self._commandsockets[socket_index].connect((host, port))
            self._commandsocketsf.append(self._commandsockets[socket_index].makefile('r'))
            answ = self._commandsocketsf[socket_index].readline()
            self.sendget("SET CONNECTIONMODE SRCP COMMAND", socket_index)
            self.sendget("GO", socket_index)
            return f'Openend command socket {socket_index}: {answ}'
        except socket.error:
            self._commandsockets[socket_index].close()
            self._commandsockets = self._commandsockets[0:socket_index]
            raise

    def connected(self, socket_index: int = 0) -> bool:
        # Connection to server established?
        return len(self._commandsockets) >= socket_index + 1

    def send(self, cmd: str, socket_index: int = 0):
        """
        Send a command to the SRCP server.
        """
        log.debug(f'SRCP sending on command socket {socket_index}: {cmd}')

        if not self.connected(socket_index):
            raise SrcpError('not connected')
        self._commandsockets[socket_index].send(f'{cmd}\n')

    def sendget(self, cmd: str, socket_index: int = 0) -> str:
        """

        Send a command to the SRCP server and wait for an answer.
        Exactly one text row will be returned.

        """
        self.send(cmd, socket_index)
        response: str = self._commandsocketsf[socket_index].readline()
        log.debug(f'got: {response.rstrip()}')
        return response

    @staticmethod
    def expect(a, b):
        if a != b:
            raise ProtocolError(f'{b} expected, {a} received')

    def set_power(self, p: int = 1, bus: int = 1, socket_index: int = 0):
        """Enable/disable power on the tracks"""
        if p:
            return self.sendget(f'SET {bus} POWER ON', socket_index)
        else:
            return self.sendget(f'SET {bus} POWER OFF', socket_index)

    def get_power(self, bus: int = 1, socket_index: int = 0) -> int:
        """Determine the current setting of the power switch (see power())"""
        response = self.sendget(f'GET {bus} POWER', socket_index).split()
        if len(response) < 6:
            raise ProtocolError(f'{response} not expected')
        self.expect(response[2], "INFO")
        self.expect(int(response[3]), bus)
        self.expect(response[4], "POWER")
        if response[5] == "ON":
            return 1
        if response[5] == "OFF":
            return 0
        raise ProtocolError("ON/OFF expected, %response received" % response[2])

    def get_FB(self, portnr: int, bus: int = 1, socket_index: int = 0) -> int:
        response = self.sendget(f'GET {bus} FB {portnr}', socket_index).split()
        if not response:
            return 0
        if len(response) != 7:
            raise ProtocolError(f'{response} not expected')
        self.expect(response[2], "INFO")
        self.expect(int(response[3]), bus)
        self.expect(response[4], "FB")
        self.expect(int(response[5]), portnr)
        return int(response[6])

    def wait_FB(self, portnr: int, state: int, timeout: int, socket_index: int = 0, bus: int = 1) -> str:
        """wait until fb goes into given state. wait at most timeout seconds"""
        return self.sendget(f'WAIT {bus} FB {portnr} {state} {timeout}', socket_index)

    def set_FB(self, portnr: int, state: int, bus: int = 1, socket_index: int = 0):
        s = self.sendget(f'SET {bus} FB {portnr} {state}', socket_index)

    def add_loco(self, loco):
        """add_loco(self, l)

        Define a new loco l of type class Loco.
        The deviceprotocol and address are used to distinguish all the locos.
        Information sent through the info port is dispatched to the loco
        to update its state to match the actual state.

        """
        locoident = f'{loco.getAddress()}/{loco.getBus()}'
        log.debug('storing loco [%s] with ident %s' % (loco, locoident))
        self._locos[locoident] = loco

    def add_accessory(self, accessory, address=None):
        """addAccessory(self, a)

        Define a new accessory a of type class Accessory.  The
        decodertype and address are used to distinguish all the
        accessories.  Information sent through the info port is
        dispatched to the accessory to update its state to match the
        actual state.

        """
        if address is None:
            address = accessory.getAddress()

        accident = '%d/%d' % (address, accessory.getBus())
        log.debug('storing accessory [%s] with ident %s' % (accessory, accident))
        self._accessories[accident] = accessory

    def open_info_port(self):
        """OpenInfoPort(self)

        Open the info port of the SRCP server.
        This function is normally used in conjunction with
        ReadDispatchInfo().
        The method Monitor() is used to asynchronously
        process incoming info messages.

        """
        log.debug('OpenInfoPort: %s %s' % (self.host, self.port))
        if not self.connected:
            raise SrcpError('not connected')
        if self._InfoportS:
            raise SrcpError('infoport already open')
        self._InfoportS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._InfoportS.connect((self.host, self.port))
            self._InfoportF = self._InfoportS.makefile('r')
            answ = self._InfoportF.readline()
            self._InfoportS.send(b'SET CONNECTIONMODE SRCP INFO\n')
            self._InfoportF.readline()
            self._InfoportS.send(b'GO\n')
            self._InfoportF.readline()
            return answ
        except socket.error:
            self._InfoportS.close()
            self._InfoportS = None
            raise


    def getInfoPortSocket(self):
        return self._InfoportS

    def addFBProc(self, portno, proc, bus=1):
        if bus not in self._fb_procs:
            self._fb_procs[bus] = {}
        if portno in self._fb_procs[bus]:
            self._fb_procs[bus][portno].append(proc)
        else:
            self._fb_procs[bus][portno] = [proc]

    def clearFBProc(self, portno, bus=1):
        if bus in self._fb_procs:
            if portno in self._fb_procs[bus]:
                del self._fb_procs[bus][portno]

    def addGAProc(self, proc):
        self._ga_procs.append(proc)

    def setTimerProc(self, timeout, proc):
        self._timeoutproc = [timeout, proc]

    def addInputProc(self, file, proc):
        self._inputProc = (file, proc)

    def readDispatchInfo(self):
        """ReadDispatchInfo(self)
        Read and dispatch all the data currently available on the info port.
        """

        # read some lines
        datalines = string.split(self._InfoportS.recv(65536), '\n')
        for data in datalines:
            log.debug('Monitor info: %s' % data)
            # print('Monitor info: %s' % data)
            if not data: continue
            w = string.split(data)
            if w[2] != 'INFO': continue

            if w[4] == 'GL':
                locoident = w[5] + '/' + w[3]
                if locoident in self._locos:
                    self._locos[locoident].parseinfo(data)
            elif w[4] == 'GA':
                accident = w[5] + '/' + w[3]
                if accident in self._accessories:
                    self._accessories[accident].parseinfo(data)
                if w[1] == '100':
                    for proc in self._ga_procs:
                        #    acc_nr     bus, acc_port   state
                        proc(int(w[5]), int(w[3]), int(w[6]), int(w[7]))
            elif w[4] == 'FB':
                portno = int(w[5])
                bus = int(w[3])
                if bus in self._fb_procs:
                    if portno in self._fb_procs[bus]:
                        proclist = self._fb_procs[bus][portno]
                        for proc in proclist:
                            proc(portno, bus, int(w[6]))

    def mainloop(self):
        log.debug('InMonitor!')
        selectports = []
        self.open_info_port()
        selectports.append(self._InfoportS)

        if self._inputProc[0] != None:
            selectports.append(self._inputProc[0])

        log.debug('Monitor: ports: ' + repr(selectports))
        t = self._timeoutproc[0]
        while (1):
            readable, w, x, t = xselect(selectports, [], [], t)
            if self._InfoportS in readable:
                self.readDispatchInfo()
                continue
            if self._inputProc[0] in readable:
                self._inputProc[1]()
                continue
            assert t <= 0, "implementation error"
            if self._timeoutproc[1] != None:
                # noch ungetestet, deshalb auskommentiert
                # self.__timeoutproc[1]()
                t = self._timeoutproc[0]

    def monitor(self):
        import threading
        t = threading.Thread(target=self.mainloop)
        t.setDaemon(1)
        t.start()

    # Funktioniert nicht mit srcpd V.2.0.10: RESET 0 SERVER
    #  def reset(self):
    #    """Re-initialize the server"""
    #    self.send("RESET 0 SERVER")
