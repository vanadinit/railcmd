# import socket
# import string
# from time import sleep

from railcmd.connection import SrcpConnection

srcp = SrcpConnection()


def Connect(host='localhost', port=4303):
    """Establish a connection to the SRCP-server

    host and port specifiy the parameters of how to connect the server.
    If the connection could not be established the according exception
    will be raised.

    """
    return srcp.connect(host, port)


def Power(p=1, bus=1):
    """Enable/disable power on the tracks"""
    srcp.set_power(p, bus)


def GetPower(bus=1):
    """Determine the curret setting of the power switch (see Power())"""
    return srcp.get_power(bus)


def Monitor():
    """Start the moonitor to dispatch messages on info/poll-port
    pollport may be None to disable the port.
    """
    srcp.monitor()

    # def Reset():
    """Re-initialize the server"""

#    srcp.reset()
#
# ######################################################################
#
# class accessory:
#     """
#     General handling of an accessory of type NMRA or Mï¿½klin or PS
#     """
#
#     def __init__(self, addr, decodertype, decodername, delay=-20,
#                  srcp=srcp, bus=1, socket_index=0):
#         self.__addr = addr
#         self.__decodertype = decodertype
#         self.__decodername = decodername
#         self.__delay = delay
#         self.__state = 0
#         self.__action = 0
#         self.__srcp = srcp
#         self.__bus = bus
#
#         srcp.add_accessory(self)
#
#         r = srcp.sendget("INIT %d GA %s %s" %
#                          (self.__bus, self.__addr, self.__decodertype), socket_index)
#
#     def __str__(self):
#         return 'Accessory %s: %s Bus %d State %d Action %d' % (self.__decodertype,
#                                                                self.__addr, self.__bus, self.__state, self.__action)
#
#     def valueChanged(self):
#         # called whenever state changes by info message from server
#         # may be overridden by subclassing or by redefinition in object.
#         pass
#
#     def parseinfo(self, info):
#         log.debug('parseinfo')
#         i = string.split(info)
#         assert i[2] == 'INFO'
#         assert i[3] == str(self.__bus)
#         assert i[4] == 'GA'
#         assert i[5] == str(self.__addr)
#
#         if i[1] == '100':
#             self.__state = int(i[6])
#             self.__action = int(i[7])
#         elif i[1] == '101':
#             assert i[6] == self.__decodertype
#         else:
#             raise ProtocolError("Answer code %s not expected." % i[1])
#             self.valueChanged()
#
#     def getDecodertype(self):
#         """get decodertype e.g. 'M'"""
#         return self.__decodertype
#
#     def getBus(self):
#         """get Bus"""
#         return self.__bus
#
#     def actuate(self, port, action=1, socket_index=0):
#         """activate the accessory
#
#         An accessory has two ports (0 and 1). actuate activates
#         (action=1) or deactivates (action=0) one of these ports.
#         Normally deactivation is done automatically by the srcp-server
#         of by this method actuate (see setDelay).
#         """
#         if self.__delay == None:
#             # don't use automatic switch off
#             self.__srcp.sendget('SET %d GA %s %s %s -1' % (
#                 self.__bus, self.__addr, port, action), socket_index)
#             return
#
#         self.__srcp.sendget('SET %d GA %s %s %s %s' % (
#             self.__bus, self.__addr, port,
#             action, max(-1, self.__delay)), socket_index)
#         if action and self.__delay < 0:
#             sleep(self.__delay / -1000.0)
#             self.__srcp.sendget('SET %d GA %s %s 0 -1' % (
#                 self.__bus, self.__addr, port), socket_index)
#         self.__state = port
#
#     def setDelay(self, newDelay):
#         """Set the delay to automatically switch off the actuator activation
#
#         The time is given in milli-seconds.
#         Positive values delegate the treatment to the SRCP-server.
#         Negative values result in a local handling: The accessory waits
#         itself until the time passed and afterwards switches off the
#         actuator command.
#         The special value None is used to disable autmatic switch off.
#         """
#         self.__delay = newDelay
#
#     def hp0(self, socket_index=0):
#         """a shortcut for self.actuate(0)"""
#         self.actuate(0, socket_index=socket_index)
#
#     set = hp0
#
#     def hp1(self, socket_index=0):
#         """a shortcut for self.actuate(1)"""
#         self.actuate(1, socket_index=socket_index)
#
#     reset = hp1
#
#     def toggle(self, socket_index=0):
#         """toggles the current state of the accessory"""
#         self.actuate(int(not self.__state), socket_index=socket_index)
#         return self.__state
#
#     def getState(self):
#         """returns the current state of the accessory"""
#         return [self.__state, self.__action]
#
#     def getAddress(self):
#         return self.__addr
#
#
# class accessoryM(accessory):
#     """
#     Specialized accessory of type Mï¿½klin
#     """
#
#     def __init__(self, addr, bus=1, delay=-20, srcp=srcp):
#         accessory.__init__(self, addr, 'M', 'Maerklin Acc', delay, srcp, bus)
#
#
# turnoutM = signalM = accessoryM
#
#
# class accessoryN(accessory):
#     """
#     Spezialized accessory of type NMRA
#     """
#
#     def __init__(self, addr, bus=1, delay=-20, socket_index=0, srcp=srcp):
#         accessory.__init__(self, addr, 'N', 'NMRA DCC Acc', delay, srcp,
#                            bus, socket_index)
#
#
# turnoutN = signalN = accessoryN
#
#
# class accessoryP(accessory):
#     """
#     Spezialized accessory of type P
#     """
#
#     def __init__(self, addr, bus=1, delay=-20, socket_index=0, srcp=srcp):
#         accessory.__init__(self, addr, 'P', 'Protocol by server', delay,
#                            srcp, bus, socket_index)
#
#
# turnoutP = signalP = accessoryP
#
#
# def mhp0(n, srcp=srcp): signalM(n, srcp=srcp).hp0()
#
#
# def mhp1(n, srcp=srcp): signalM(n, srcp=srcp).hp1()
#
#
# def nhp0(n, srcp=srcp): signalN(n, srcp=srcp).hp0()
#
#
# def nhp1(n, srcp=srcp): signalN(n, srcp=srcp).hp1()
#
#
# def php0(n, srcp=srcp): signalP(n, srcp=srcp).hp0()
#
#
# def php1(n, srcp=srcp): signalP(n, srcp=srcp).hp1()
#
#
# mset = mhp0
# mreset = mhp1
# nset = nhp0
# nreset = nhp1
# pset = nhp0
# preset = nhp1
#
#
# class hsignal(accessory):
#     """
#
#     """
#
#     def __init__(self, base_address, decodertype, decodername,
#                  hp0_code, hp1_code, hp2_code, sh1_code,
#                  srcp=srcp, bus=1, socket_index=0):
#
#         addresslist = []
#
#         for code in [hp0_code, hp1_code, hp2_code, sh1_code]:
#             if len(code) > 0:
#                 addresslist.append(base_address + code[0])
#
#         # remove doubles
#         addresslist = list(set(addresslist))
#
#         self.__base_address = base_address
#         self.__addresslist = addresslist
#
#         self.__codes = [hp0_code, hp1_code, hp2_code, sh1_code]
#
#         self.__decodertype = decodertype
#         self.__decodername = decodername
#
#         self.__state = 0  # state of signal 0:hp0 1:hp1 2:hp2 3:sh1
#
#         self.__srcp = srcp
#         self.__bus = bus
#
#         for address in addresslist:
#             r = srcp.sendget("INIT %d GA %s %s"
#                              % (self.__bus, address, self.__decodertype), socket_index)
#             srcp.add_accessory(self, address)
#
#     def __str__(self):
#         string = ('Hauptsignal with state %s consisting of the following adresses:'
#                   % self.getState())
#         for i_addr in range(len(self.__addresslist)):
#             address = self.__addresslist[i_addr]
#             string = string + '\n' + ('Accessory %s: %s Bus %d'
#                                       % (self.__decodertype, address, self.__bus))
#
#         string = string + '\nCodes: ' + str(self.__codes)
#         return string
#
#     def valueChanged(self):
#         # called whenever state changes by info message from server
#         # may be overridden by subclassing or by redefinition in object.
#         pass
#
#     def parseinfo(self, info):
#         log.debug('parseinfo')
#         i = string.split(info)
#
#         # print info
#
#         # For Signal the initial states sent by the sprcd after connecting are
#         # not correct.
#         # Howerver, these are sent with time smaller 1.0
#         # temporal solution: omit these infos
#         if float(i[0]) <= 1.0:
#             return
#
#         assert i[2] == 'INFO'
#         assert i[3] == str(self.__bus)
#         assert i[4] == 'GA'
#         address = int(i[5])
#         assert address in self.__addresslist
#
#         if i[1] == '100':
#             address_index = self.__addresslist.index(address)
#             state = int(i[6])
#             action = int(i[7])
#
#             for icode in range(len(self.__codes)):
#                 if len(self.__codes[icode]) == 3:
#                     if [address - self.__base_address, state, action] == self.__codes[icode]:
#                         # code found!
#                         self.__state = icode
#                         break
#                 else:
#                     if [address - self.__base_address, state] == self.__codes[icode]:
#                         # code found!
#                         self.__state = icode
#                         # print('erkannt: Signal %d Zustand %s' % (self.__base_address,self.getState()))
#                         break
#
#         elif i[1] == '101':
#             assert i[6] == self.__decodertype
#         else:
#             raise ProtocolError("Answer code %s not expected." % i[1])
#
#         self.valueChanged()
#
#     def getDecodertype(self):
#         """get decodertype e.g. 'M'"""
#         return self.__decodertype
#
#     def getBus(self):
#         """get Bus"""
#         return self.__bus
#
#     def actuate(self, port, action=1, socket_index=0):
#         pass
#
#     def setDelay(self, newDelay):
#         pass
#
#     def hp0(self):
#         pass
#
#     def hp1(self):
#         pass
#
#     def toggle(self):
#         pass
#
#     def getState(self):
#         """returns the current state of the accessory"""
#         if self.__state == 0:
#             return 'hp0'
#         elif self.__state == 1:
#             return 'hp1'
#         elif self.__state == 2:
#             return 'hp2'
#         elif self.__state == 3:
#             return 'sh1'
#         else:
#             return 'unknown state'
#
#     def getAddress(self):
#         pass
#
#
# ######################################################################
#
# class Feedback:
#     """
#     General class to handle feedback devices
#     """
#
#     __state = 0
#
#     def __init__(self, portnr, bus=1, srcp=srcp):
#         self.__portnr = portnr
#         self.__srcp = srcp
#         self.__bus = bus
#
#     def __str__(self):
#         r = 'Feedback %d Bus %d: %d' % (self.__portnr, self.__bus, self.__state)
#         return r
#
#     def getBus(self):
#         """get Bus"""
#         return self.__bus
#
#     def expect(self, a, b):
#         if a != b:
#             raise ProtocolError('%s expected, got %s' % (b, a))
#
#     def getState(self, socket_index=0):
#         return self.__srcp.get_FB(self.__portnr, self.__bus, socket_index)
#         # return self.__state
#
#     def setState(self, state, socket_index=0):
#         self.__srcp.set_FB(self.__portnr, state, self.__bus, socket_index)
#
#     def wait(self, state, timeout, socket_index=0):
#         """wait until fb goes into given state. wait at most timeout seconds"""
#         r = self.__srcp.wait_FB(self.__portnr, state, timeout, socket_index, self.__bus)
#         self.parseinfo(r)
#         return self.__state
#
#     def parseinfo(self, info):
#         if not info: return
#         i = string.split(info)
#         if i[2] == 'INFO':  ##else: timeout
#             self.expect(i[1], '100')
#             self.expect(i[3], str(self.__bus))
#             self.expect(i[4], 'FB')
#             self.expect(i[5], str(self.__portnr))
#             self.__state = int(i[6])
#
#         ######################################################################
#
#
# class parseinfo:
#     """
#     Abstract class which is able to interpret info messages sent from
#     the SRCP server. Instances of this class have to be added to to
#     srcp_connection using addLoco(). scrp_connection then calls parseinfo()
#     whenever new info for this instance arrives.
#     """
#
#     def __init__(self):
#         pass
#
#     def expect(self, a, b):
#         if a != b:
#             raise ProtocolError('%s expected, got %s' % (b, a))
#
#     def valueChanged(self):
#         # called whenever state changes by info message from server
#         # may be overridden by subclassing or by redefinition in object.
#         pass
#
#     def parseinfo(self, info):
#         log.debug('parseinfo')
#         # if not info: return
#         i = string.split(info)
#         assert i[2] == 'INFO'
#         assert i[3] == str(self.getBus())
#         assert i[4] == 'GL'
#         assert i[5] == str(self.getAddress())
#
#         if i[1] == '101':
#             assert i[6] == self.getDeviceprotocol()
#             assert i[7] == self.getProtocolversion()
#             assert i[8] == str(self.getNumfunctions() + 1)
#             # Ignoring maxSpeed here in i[9]
#
#         elif (i[1] == '100'):
#             if (not self.has_unapplied_changes()):
#                 # only update loco if there are no unapplied changes
#                 i6 = list(map(int, i[6:]))
#                 # i6: [<direction> <V> <V_max> <func> <f1> .. <fn>]
#                 if int(i6[0] != 2):  # kein Nothalt
#                     self.setDirection(i6[0], parsemode=1)
#                     # normalize external speed to internal speed (differing max speeds)
#                 self.setSpeed((i6[1] * self._maxspeed + i6[2] / 2) / i6[2], parsemode=1)
#
#                 self.setFunction(i6[3], parsemode=1)
#                 for n in range(1, self.getNumfunctions() + 1):
#                     self.setF(n, i6[4 + n - 1], parsemode=1)
#
#         else:
#             raise ProtocolError("Answer code %s not expected." % i[1])
#
#         log.debug('parseinfo: %s' % self)
#         self.valueChanged()
#
#
# ######################################################################
#
# class Loco(parseinfo):
#     """
#     General class to drive locomotives.
#     """
#     __dir = 1  # vorwï¿½ts
#     __speed = 0
#
#     def __init__(self, addr, deviceprotocol, protocolversion, decodername, maxspeed,
#                  numfunctions, srcp=srcp, bus=1, socket_index=0):
#         parseinfo.__init__(self)
#         self.__addr = addr
#         self.__deviceprotocol = deviceprotocol
#         self.__protocolversion = protocolversion
#         self.__decodername = decodername
#         self._maxspeed = self.__decodermaxspeed = maxspeed
#         self.__numfunctions = numfunctions
#         self.__f = [0] * (numfunctions + 1)
#         self.__srcp = srcp
#         self.__bus = bus
#         self.__has_unapplied_changes = 0
#
#         # Look if loco yet exists or not
#         r = self.__srcp.sendget('GET %d GL %d'
#                                 % (bus, addr), socket_index)
#         rsp = string.split(r)
#
#         if rsp[2] == 'INFO':
#             # loco exits, get existing data
#             self.parseinfo(r)
#         else:
#             # loco does not exist yet, initialise it
#             self.__srcp.sendget('INIT %d GL %d %s %s %d %d'
#                                 % (bus, addr, deviceprotocol, protocolversion,
#                                    maxspeed, numfunctions + 1))
#
#         self.__srcp.add_loco(self)
#
#     def __str__(self):
#         r = 'Loco addr: %d, bus: %d, decoder: %s%s, dir: %d speed: %d, ' \
#             'functions:' % (
#                 self.__addr, self.__bus, self.__deviceprotocol, self.__protocolversion,
#                 self.__dir, self.__speed)
#         for i in range(self.__numfunctions + 1):
#             r = r + ' %d' % self.__f[i]
#         return r
#
#     def getBus(self):
#         """get Bus"""
#         return self.__bus
#
#     def has_unapplied_changes(self):
#         return self.__has_unapplied_changes
#
#     def send(self, socket_index=0):
#         self.__srcp.sendget(self.srcp(), socket_index)
#         self.__has_unapplied_changes = 0
#
#     def setSpeed(self, s, parsemode=0):
#         """set speed setting
#         # parsemode: speedSetting by dispatching INFO-port and not
#         # by user
#
#         The specified speed has to be in range 0..maxspeed
#
#         """
#         log.debug('addr %d, bus %d: setSpeed %s'
#                   % (self.__addr, self.__bus, s))
#         assert 0 <= s <= self._maxspeed
#         self.__speed = s
#         if not parsemode:
#             self.__has_unapplied_changes = 1
#
#     def getSpeed(self):
#         """get speed setting"""
#         log.debug('addr %d, bus %d: getSpeed'
#                   % (self.__addr, self.__bus))
#         return self.__speed
#
#     def getNumFunctions(self):
#         """get number of supported functions by decoder"""
#         return self.__numfunctions
#
#     numfunctions = getNumFunctions
#
#     def getFunction(self):
#         """get setting of FUNCTION"""
#         log.debug('%d: getFunction %s' % (self.__addr, self.__f[0]))
#         return self.__f[0]
#
#     def setFunction(self, v, parsemode=0):
#         """set/get setting of FUNCTION"""
#         log.debug('addr %d, bus %d: setFunction %s->%s' %
#                   (self.__addr, self.__bus, self.__f[0], v))
#         assert v == 0 or v == 1
#         self.__f[0] = v
#         if not parsemode:
#             self.__has_unapplied_changes = 1
#
#     def toggleFunction(self, parsemode=0):
#         """toggle setting of FUNCTION"""
#         log.debug('addr %d, bus %d: toggleFunction %s'
#                   % (self.__addr, self.__bus, self.__f[0]))
#         self.__f[0] = int(not self.__f[0])
#         if not parsemode:
#             self.__has_unapplied_changes = 1
#
#     def setF(self, n, v, parsemode=0):
#         """set Fn to v"""
#         log.debug('addr %d, bus %d: setF %d %s->%s'
#                   % (self.__addr, self.__bus, n, self.__f[n], v))
#         assert 0 <= n <= self.__numfunctions + 1
#         assert v == 0 or v == 1
#         self.__f[n] = v
#         if not parsemode:
#             self.__has_unapplied_changes = 1
#
#     def getF(self, n):
#         """get value of Fn"""
#         log.debug('addr %d, bus %d: getF %s'
#                   % (self.__addr, self.__bus, self.__f[n]))
#         assert 0 <= n <= self.__numfunctions
#         return self.__f[n]
#
#     def getFList(self):
#         """get list of all Fn (incl. Func)"""
#         log.debug('addr %d, bus %d: getFList %s'
#                   % (self.__addr, self.__bus, self.__f))
#         return self.__f[:]
#
#     def setFList(self, v, parsemode=0):
#         """set list of all Fn (incl. Func)"""
#         log.debug('addr %d, bus %d: setFList %s->%s'
#                   % (self.__addr, self.__bus, self.__f, v))
#         assert len(v) == self.__numfunctions + 1
#         assert reduce(lambda a, b: a and (b == 0 or b == 1), v), \
#             "boolean values expected"
#         self.__f = v[:]
#         if not parsemode:
#             self.__has_unapplied_changes = 1
#
#     def toggleF(self, n, parsemode=0):
#         """toggle value of Fn"""
#         log.debug('addr %d, bus %d: toggleF %d %s'
#                   % (self.__addr, self.__bus, n, self.__f[n]))
#         assert 0 <= n <= self.__numfunctions
#         self.__f[n] = int(not self.__f[n])
#         if not parsemode:
#             self.__has_unapplied_changes = 1
#
#     def getDecodertype(self):
#         """get Decodertype e.g. 'M2'"""
#         return self.__deviceprotocol + self.__protocolversion
#
#     def getDeviceprotocol(self):
#         return self.__deviceprotocol
#
#     def getProtocolversion(self):
#         """get Decodertype e.g. 'M2'"""
#         return self.__protocolversion
#
#     def getNumfunctions(self):
#         return self.__numfunctions
#
#     def getDecoderDescription(self):
#         """get decoder name e.g. 'M2 Maerklin new'"""
#         return self.__decodername
#
#     def getAddress(self):
#         """get address of decoder"""
#         return self.__addr
#
#     def getDecoderMaxSpeed(self):
#         """get maximum speed level supported by decoder"""
#         return self.__decodermaxspeed
#
#     def setMaxSpeed(self, s):
#         """set maximum virtual speed"""
#         if s < 0: s = self.__decodermaxspeed
#         self._maxspeed = s
#
#     def getMaxSpeed(self, s=None):
#         """get maximum virtual speed"""
#         return self._maxspeed
#
#     def getDirection(self):
#         """get direction"""
#         log.debug('addr %d, bus %d: getDirection: %d'
#                   % (self.__addr, self.__bus, self.__dir))
#         return self.__dir
#
#     def setDirection(self, d, parsemode=0):
#         """set direction"""
#         log.debug('addr %d, bus %d: setDirection %d->%s' %
#                   (self.__addr, self.__bus, self.__dir, d))
#         assert d == 0 or d == 1
#         self.__dir = d
#         if not parsemode:
#             self.__has_unapplied_changes = 1
#
#     def toggleDirection(self, parsemode=0):
#         """toggle direction"""
#         log.debug('addr %d, bus %d: setDirection %d->%s' %
#                   (self.__addr, self.__bus, self.__dir,
#                    int(not self.__dir)))
#         self.__dir = int(not self.__dir)
#         if not parsemode:
#             self.__has_unapplied_changes = 1
#
#     def srcp(self):
#         r = 'SET %d GL %s %s %s %s %s' % (self.__bus,
#                                           self.__addr, self.__dir, abs(self.__speed),
#                                           self._maxspeed, self.__f[0])
#         for i in self.__f[1:]:
#             r = r + " " + repr(i)
#         return r
#
#     def stop(self, socket_index=0):
#         # Perform an emergeny stop
#         r = 'SET %d GL %s 2 0 %s %s' % (
#             self.__bus,
#             self.__addr,
#             self._maxspeed, self.__f[0])
#         for i in self.__f[1:]:
#             r = r + " " + repr(i)
#
#         self.__srcp.sendget(r, socket_index)
#
#         self.__speed = 0
#
#         # Send normal data again to maintain data equality
#         # between real loco and object
#         self.send(socket_index)
#
#     def sendSpeed(self, speed, socket_index=0):
#         # Set AND send speed
#         self.setSpeed(speed)
#         self.send(socket_index)
#
#
# class locoM1(Loco):
#     """
#     Drive M1 locomotive
#
#     M1: Old Maerklin protocol with 14 speed steps, 0 special functions
#     """
#
#     def __init__(self, addr, bus=1, socket_index=0, srcp=srcp):
#         Loco.__init__(self, addr,
#                       'M', '1', 'M1 Maerklin old', 14, 0, srcp, bus)
#
#
# class locoM2(Loco):
#     """
#     Drive M2 locomotive
#
#     M2: New Maerklin protocol with 14 speed steps, 4 special functions
#     """
#
#     def __init__(self, addr, bus=1, socket_index=0, srcp=srcp):
#         Loco.__init__(self, addr,
#                       'M', '2', 'M2 Maerklin new', 14, 4, srcp, bus)
#
#
# class locoM3(Loco):
#     """
#     Drive M3 locomotive
#
#     M3: Special Maerklin (Wikinger) protocol with 14 speed steps,
#     4 special functions
#     """
#
#     def __init__(self, addr, bus=1, socket_index=0, srcp=srcp):
#         Loco.__init__(self, addr,
#                       'M', '2', 'M3 Maerklin (Wikinger)', 28, 4, srcp, bus)
#
#
# class locoM4(Loco):
#     """
#     Drive M4 locomotive
#
#     M4: Maerklin protocol (Uhlenbrock) with 14 speed steps,
#     4 special functions
#     """
#
#     def __init__(self, addr, bus=1, socket_index=0, srcp=srcp):
#         Loco.__init__(self, addr,
#                       'M', '2', 'M4 Maerklin (Uhlenbrock)', 14, 4, srcp, bus)
#
#
# class locoM5(Loco):
#     """
#     Drive M5 locomotive
#
#     M5: New Maerklin protocol with 27 speed steps, 4 special functions
#     """
#
#     def __init__(self, addr, bus=1, socket_index=0, srcp=srcp):
#         Loco.__init__(self, addr,
#                       'M', '2', 'M5 Maerklin new 27FS', 27, 4, srcp, bus)
#
#
# class locoN1(Loco):
#     """
#     Drive N1 locomotive
#
#     NB: NB NMRA 7bit, 28 speed steps, 4 special functions
#     """
#
#     def __init__(self, addr, bus=1, socket_index=0, srcp=srcp):
#         Loco.__init__(self, addr,
#                       'N', '1', 'N1 NMRA 7bit, 28 FS', 28, 4, srcp, bus)
#
#
# class locoN2(Loco):
#     """
#     Drive N2 locomotive
#
#     NB: NB NMRA 7bit, 128 speed steps, 4 special functions
#     """
#
#     def __init__(self, addr, bus=1, socket_index=0, srcp=srcp):
#         Loco.__init__(self, addr,
#                       'N', '2', 'N2 NMRA 7bit, 128 FS', 128, 4, srcp, bus)
#
#
# class locoP(Loco):
#     """
#     Drive PS locomotive
#
#     PS: Protocol by server.
#     """
#
#     def __init__(self, addr, bus=1, socket_index=0, srcp=srcp):
#         Loco.__init__(self, addr,
#                       'P', '1', 'Protocol by server', 126, 4, srcp, bus)
