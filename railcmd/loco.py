from functools import reduce

from .base import log
from .exceptions import ProtocolError


class parseinfo:
    """
    Abstract class which is able to interpret info messages sent from
    the SRCP server. Instances of this class have to be added to to
    srcp_connection using addLoco(). scrp_connection then calls parseinfo()
    whenever new info for this instance arrives.
    """

    def valueChanged(self):
        # called whenever state changes by info message from server
        # may be overridden by subclassing or by redefinition in object.
        pass

    def parseinfo(self, info: str):
        log.debug('parseinfo')
        # if not info: return
        i = info.split()
        assert i[2] == 'INFO'
        assert i[3] == str(self.getBus())
        assert i[4] == 'GL'
        assert i[5] == str(self.getAddress())

        if i[1] == '101':
            assert i[6] == self.getDeviceprotocol()
            assert i[7] == self.getProtocolversion()
            assert i[8] == str(self.getNumfunctions() + 1)
            # Ignoring maxSpeed here in i[9]

        elif (i[1] == '100'):
            if (not self.has_unapplied_changes()):
                # only update loco if there are no unapplied changes
                i6 = list(map(int, i[6:]))
                # i6: [<direction> <V> <V_max> <func> <f1> .. <fn>]
                if int(i6[0] != 2):  # kein Nothalt
                    self.setDirection(i6[0], parsemode=1)
                    # normalize external speed to internal speed (differing max speeds)
                self.setSpeed((i6[1] * self._maxspeed + i6[2] / 2) / i6[2], parsemode=1)

                self.setFunction(i6[3], parsemode=1)
                for n in range(1, self.getNumfunctions() + 1):
                    self.setF(n, i6[4 + n - 1], parsemode=1)

        else:
            raise ProtocolError("Answer code %s not expected." % i[1])

        log.debug('parseinfo: %s' % self)
        self.valueChanged()


######################################################################

class Loco(parseinfo):
    """
    General class to drive locomotives.
    """
    __dir = 1  # vorwärts
    __speed = 0

    def __init__(self, addr, deviceprotocol, protocolversion, decodername, maxspeed,
                 numfunctions, srcp, bus=1, socket_index=0):
        self.__addr = addr
        self.__deviceprotocol = deviceprotocol
        self.__protocolversion = protocolversion
        self.__decodername = decodername
        self._maxspeed = self.__decodermaxspeed = maxspeed
        self.__numfunctions = numfunctions
        self.__f = [0] * (numfunctions + 1)
        self.__srcp = srcp
        self.__bus = bus
        self.__has_unapplied_changes = 0

        # Look if loco yet exists or not
        r = self.__srcp.sendget('GET %d GL %d'
                                % (bus, addr), socket_index)
        rsp = r.split()

        if rsp[2] == 'INFO':
            # loco exits, get existing data
            self.parseinfo(r)
        else:
            # loco does not exist yet, initialise it
            self.__srcp.sendget('INIT %d GL %d %s %s %d %d'
                                % (bus, addr, deviceprotocol, protocolversion,
                                   maxspeed, numfunctions + 1))

        self.__srcp.add_loco(self)

    def __str__(self):
        r = 'Loco addr: %d, bus: %d, decoder: %s%s, dir: %d speed: %d, ' \
            'functions:' % (
                self.__addr, self.__bus, self.__deviceprotocol, self.__protocolversion,
                self.__dir, self.__speed)
        for i in range(self.__numfunctions + 1):
            r = r + ' %d' % self.__f[i]
        return r

    def getBus(self):
        """get Bus"""
        return self.__bus

    def has_unapplied_changes(self):
        return self.__has_unapplied_changes

    def send(self, socket_index=0):
        self.__srcp.sendget(self.srcp(), socket_index)
        self.__has_unapplied_changes = 0

    def setSpeed(self, s, parsemode=0):
        """set speed setting
        # parsemode: speedSetting by dispatching INFO-port and not
        # by user

        The specified speed has to be in range 0..maxspeed

        """
        log.debug('addr %d, bus %d: setSpeed %s'
                  % (self.__addr, self.__bus, s))
        assert 0 <= s <= self._maxspeed
        self.__speed = s
        if not parsemode:
            self.__has_unapplied_changes = 1

    def getSpeed(self):
        """get speed setting"""
        log.debug('addr %d, bus %d: getSpeed'
                  % (self.__addr, self.__bus))
        return self.__speed

    def getNumFunctions(self):
        """get number of supported functions by decoder"""
        return self.__numfunctions

    numfunctions = getNumFunctions

    def getFunction(self):
        """get setting of FUNCTION"""
        log.debug('%d: getFunction %s' % (self.__addr, self.__f[0]))
        return self.__f[0]

    def setFunction(self, v, parsemode=0):
        """set/get setting of FUNCTION"""
        log.debug('addr %d, bus %d: setFunction %s->%s' %
                  (self.__addr, self.__bus, self.__f[0], v))
        assert v == 0 or v == 1
        self.__f[0] = v
        if not parsemode:
            self.__has_unapplied_changes = 1

    def toggleFunction(self, parsemode=0):
        """toggle setting of FUNCTION"""
        log.debug('addr %d, bus %d: toggleFunction %s'
                  % (self.__addr, self.__bus, self.__f[0]))
        self.__f[0] = int(not self.__f[0])
        if not parsemode:
            self.__has_unapplied_changes = 1

    def setF(self, n, v, parsemode=0):
        """set Fn to v"""
        log.debug('addr %d, bus %d: setF %d %s->%s'
                  % (self.__addr, self.__bus, n, self.__f[n], v))
        assert 0 <= n <= self.__numfunctions + 1
        assert v == 0 or v == 1
        self.__f[n] = v
        if not parsemode:
            self.__has_unapplied_changes = 1

    def getF(self, n):
        """get value of Fn"""
        log.debug('addr %d, bus %d: getF %s'
                  % (self.__addr, self.__bus, self.__f[n]))
        assert 0 <= n <= self.__numfunctions
        return self.__f[n]

    def getFList(self):
        """get list of all Fn (incl. Func)"""
        log.debug('addr %d, bus %d: getFList %s'
                  % (self.__addr, self.__bus, self.__f))
        return self.__f[:]

    def setFList(self, v, parsemode=0):
        """set list of all Fn (incl. Func)"""
        log.debug('addr %d, bus %d: setFList %s->%s'
                  % (self.__addr, self.__bus, self.__f, v))
        assert len(v) == self.__numfunctions + 1
        assert reduce(lambda a, b: a and (b == 0 or b == 1), v), \
            "boolean values expected"
        self.__f = v[:]
        if not parsemode:
            self.__has_unapplied_changes = 1

    def toggleF(self, n, parsemode=0):
        """toggle value of Fn"""
        log.debug('addr %d, bus %d: toggleF %d %s'
                  % (self.__addr, self.__bus, n, self.__f[n]))
        assert 0 <= n <= self.__numfunctions
        self.__f[n] = int(not self.__f[n])
        if not parsemode:
            self.__has_unapplied_changes = 1

    def getDecodertype(self):
        """get Decodertype e.g. 'M2'"""
        return self.__deviceprotocol + self.__protocolversion

    def getDeviceprotocol(self):
        return self.__deviceprotocol

    def getProtocolversion(self):
        """get Decodertype e.g. 'M2'"""
        return self.__protocolversion

    def getNumfunctions(self):
        return self.__numfunctions

    def getDecoderDescription(self):
        """get decoder name e.g. 'M2 Maerklin new'"""
        return self.__decodername

    def getAddress(self):
        """get address of decoder"""
        return self.__addr

    def getDecoderMaxSpeed(self):
        """get maximum speed level supported by decoder"""
        return self.__decodermaxspeed

    def setMaxSpeed(self, s):
        """set maximum virtual speed"""
        if s < 0: s = self.__decodermaxspeed
        self._maxspeed = s

    def getMaxSpeed(self, s=None):
        """get maximum virtual speed"""
        return self._maxspeed

    def getDirection(self):
        """get direction"""
        log.debug('addr %d, bus %d: getDirection: %d'
                  % (self.__addr, self.__bus, self.__dir))
        return self.__dir

    def setDirection(self, d, parsemode=0):
        """set direction"""
        log.debug('addr %d, bus %d: setDirection %d->%s' %
                  (self.__addr, self.__bus, self.__dir, d))
        assert d == 0 or d == 1
        self.__dir = d
        if not parsemode:
            self.__has_unapplied_changes = 1

    def toggleDirection(self, parsemode=0):
        """toggle direction"""
        log.debug('addr %d, bus %d: setDirection %d->%s' %
                  (self.__addr, self.__bus, self.__dir,
                   int(not self.__dir)))
        self.__dir = int(not self.__dir)
        if not parsemode:
            self.__has_unapplied_changes = 1

    def srcp(self):
        r = 'SET %d GL %s %s %s %s %s' % (self.__bus,
                                          self.__addr, self.__dir, abs(self.__speed),
                                          self._maxspeed, self.__f[0])
        for i in self.__f[1:]:
            r = r + " " + repr(i)
        return r

    def stop(self, socket_index=0):
        # Perform an emergeny stop
        r = 'SET %d GL %s 2 0 %s %s' % (
            self.__bus,
            self.__addr,
            self._maxspeed, self.__f[0])
        for i in self.__f[1:]:
            r = r + " " + repr(i)

        self.__srcp.sendget(r, socket_index)

        self.__speed = 0

        # Send normal data again to maintain data equality
        # between real loco and object
        self.send(socket_index)

    def sendSpeed(self, speed, socket_index=0):
        # Set AND send speed
        self.setSpeed(speed)
        self.send(socket_index)


class TypedLoco(Loco):
    TYPES = {
        'M1': {
            'protocol': 'M',
            'proto_version': '1',
            'decodername': 'M1 Maerklin old',
            'maxspeed': 14,
            'numfunctions': 0,
            'description': 'Old Maerklin protocol with 14 speed steps, 0 special functions',
        },
        'M2': {
            'protocol': 'M',
            'proto_version': '2',
            'decodername': 'M2 Maerklin new',
            'maxspeed': 14,
            'numfunctions': 4,
            'description': 'New Maerklin protocol with 14 speed steps, 4 special functions',
        },
        'M3': {
            'protocol': 'M',
            'proto_version': '2',
            'decodername': 'M3 Maerklin (Wikinger)',
            'maxspeed': 28,
            'numfunctions': 4,
            'description': 'Special Maerklin (Wikinger) protocol with 14 speed steps, 4 special functions',
        },
        'M4': {
            'protocol': 'M',
            'proto_version': '2',
            'decodername': 'M4 Maerklin (Uhlenbrock)',
            'maxspeed': 14,
            'numfunctions': 4,
            'description': 'Maerklin protocol (Uhlenbrock) with 14 speed steps, 4 special functions',
        },
        'M5': {
            'protocol': 'M',
            'proto_version': '2',
            'decodername': 'M5 Maerklin new 27FS',
            'maxspeed': 27,
            'numfunctions': 4,
            'description': 'New Maerklin protocol with 27 speed steps, 4 special functions',
        },
        'N1': {
            'protocol': 'N',
            'proto_version': '1',
            'decodername': 'N1 NMRA 7bit, 28 FS',
            'maxspeed': 28,
            'numfunctions': 4,
            'description': 'NB NMRA 7bit, 28 speed steps, 4 special functions',
        },
        'N2': {
            'protocol': 'N',
            'proto_version': '2',
            'decodername': 'N2 NMRA 7bit, 128 FS',
            'maxspeed': 128,
            'numfunctions': 4,
            'description': 'NB NMRA 7bit, 128 speed steps, 4 special functions',
        },
        'P': {
            'protocol': 'P',
            'proto_version': '1',
            'decodername': 'Protocol by server',
            'maxspeed': 126,
            'numfunctions': 4,
            'description': 'Protocol by server',
        },
    }

    def __init__(self, type: str, addr, srcp, bus=1, socket_index=0):
        loco_type = TypedLoco.TYPES[type]
        super().__init__(
            addr=addr,
            deviceprotocol=loco_type['protocol'],
            protocolversion=loco_type['proto_version'],
            decodername=loco_type['decodername'],
            maxspeed=loco_type['maxspeed'],
            numfunctions=loco_type['numfunctions'],
            srcp=srcp,
            bus=bus,
            socket_index=socket_index,
        )
