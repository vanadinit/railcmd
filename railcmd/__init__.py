# import socket
# import string
# from time import sleep

from railcmd.connection import SrcpConnection

srcp = SrcpConnection()


def connect(host='localhost', port=4303):
    """Establish a connection to the SRCP-server

    host and port specifiy the parameters of how to connect the server.
    If the connection could not be established the according exception
    will be raised.

    """
    return srcp.connect(host, port)


def power(p=1, bus=1):
    """Enable/disable power on the tracks"""
    srcp.set_power(p, bus)


def get_power(bus=1):
    """Determine the curret setting of the power switch (see Power())"""
    return srcp.get_power(bus)


# def Monitor():
#     """Start the moonitor to dispatch messages on info/poll-port
#     pollport may be None to disable the port.
#     """
#     srcp.monitor()
#
#     # def Reset():
#     """Re-initialize the server"""
#
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
