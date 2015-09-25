'''
Created on 23 sept. 2015

@author: b.christol
'''
# --------- Python program: XPS controller demonstration -------- #
import sys

import XPS_Q8_drivers


#import time
# Display error function: simplify error print out and closes socket



class DriversXPSQ:
    """Drivers
    """
    def __init__(self):
        print "START XPS Q8"
        try:
            # Instantiate the class
            self.myxps = XPS_Q8_drivers.XPS()
            ip = '192.168.0.201'
            port = 5001
            print 'a' 
            # Connect to the XPS
            self.socketId = self.myxps.TCP_ConnectToServer(ip, port, 20)
            print str(self.socketId) + ' :SOCKET'
            # Check connection passed
            if (self.socketId == -1):
                print 'Connection to XPS failed, check IP & Port'
                sys.exit()
            else :
                print "Connexion at %s on %d successful, continue ..." % (ip, port)
             
            # Add here your personal codes, below for example:
            # Define the positioner
            self.group = 'S1'
            self.positioner = self.group + '.AXE_X'
            # Kill the group
            [errorCode, returnString] = self.myxps.GroupKill(self.socketId, self.group)
            if (errorCode != 0):
                displayErrorAndClose (self.socketId, errorCode, 'GroupKill')
                sys.exit()
            else :
                print "GroupKill %s sucessfull" % self.group
             
            # Initialize the group
            [errorCode, returnString] = self.myxps.GroupInitialize(self.socketId, self.group)
            if (errorCode != 0):
                displayErrorAndClose (self.socketId, errorCode, 'GroupInitialize')
                sys.exit()
            else :
                print "GroupInitialize %s sucessfull" % self.group
                 
            # Home search
            [errorCode, returnString] = self.myxps.GroupHomeSearch(self.socketId, self.group)
            if (errorCode != 0):
                displayErrorAndClose (self.socketId, errorCode, 'GroupHomeSearch')
                sys.exit()
            else :
                print "GroupHomeSearch %s sucessfull" % self.group
                     
            # Enable Jog
            [errorCode, returnString] = self.myxps.GroupJogModeEnable(self.socketId, self.group)
            if (errorCode != 0):
                displayErrorAndClose (self.socketId, errorCode, 'GroupJogModeEnable')
                sys.exit()
            else :
                print "GroupJogModeEnable %s sucessfull" % self.group
                 
            # Get JOG value
            [errorCode, velocity, acceleration] = self.myxps.GroupJogParametersGet(self.socketId, self.group, 1)
            if (errorCode != 0):
                displayErrorAndClose (self.socketId, errorCode, 'GroupJogParametersGet')
                sys.exit()
            else :
                print "GroupJogParametersGet %s sucessfull" % self.group
                print "Velocity : %d" % velocity
                print "Acceleration : %d" % acceleration
        except:
            print "Failed"
           
    
    def displayErrorAndClose(self, socketId, errorCode, APIName):
        if (errorCode != -2) and (errorCode != -108):
            [errorCode2, errorString] = self.myxps.ErrorStringGet(socketId, errorCode)
            if (errorCode2 != 0):
                print APIName + ': ERROR ' + str(errorCode)
            else:
                print APIName + ': ' + errorString
        else:
            if (errorCode == -2):
                print APIName + ': TCP timeout'
            if (errorCode == -108):
                print APIName + ': The TCP/IP connection was closed by an administrator'
        self.myxps.TCP_CloseSocket(self.socketId)
        return
    
    def move_jog(self, velocity):
        #===========================================================================
        # velocity = [10]
        acceleration = [5]
        #===========================================================================
        
        # Set JOG values
        [errorCode, returnString] = self.myxps.GroupJogParametersSet(self.socketId, self.group, velocity, acceleration, 1)
        if (errorCode != 0):
            displayErrorAndClose (self.socketId, errorCode, 'GroupJogParametersSet')
            sys.exit()
        else :
            print "GroupJogParametersSet %s sucessfull" % self.group
            print "Velocity : %s" % velocity
            print "Acceleration : %s" % acceleration
         
    def get_infos(self):     
        # Get JOG value
        [errorCode, velocity, acceleration] = myxps.GroupJogParametersGet(socketId, group, 1)
        if (errorCode != 0):
            displayErrorAndClose (socketId, errorCode, 'GroupJogParametersGet')
            sys.exit()
        else :
            print "GroupJogParametersGet %s sucessfull" % group
            print "Velocity : %d" % velocity
            print "Acceleration : %d" % acceleration
        
    
        # Get groupe state value
        [errorCode, state] = myxps.GroupStatusGet(socketId, group)
        if (errorCode != 0):
            displayErrorAndClose (socketId, errorCode, 'GroupStatusGet')
            sys.exit()
        else :
            print "GroupStatusGet %s sucessfull" % group
            print "State : %s" % state
        
        
    #===============================================================================
    # velocity = [0]
    # acceleration = [0]
    # 
    # # Set JOG values
    # [errorCode, returnString] = myxps.GroupJogParametersSet(socketId, group, velocity, acceleration, 1)
    # if (errorCode != 0):
    #     displayErrorAndClose (socketId, errorCode, 'GroupJogParametersSet')
    #     sys.exit()
    # else :
    #     print "GroupJogParametersSet %s sucessfull" % group
    #     print "Velocity : %s" % velocity
    #     print "Acceleration : %s" % acceleration
    #===============================================================================
    
    def move_jog_abort(self):
        # Abort group move
        [errorCode, state] = self.myxps.GroupMoveAbort(self.socketId, self.group)
        if (errorCode != 0):
            self.displayErrorAndClose (self.socketId, errorCode, 'GroupMoveAbort')
            sys.exit()
        else :
            print "GroupMoveAbort %s sucessfull" % self.group
      
           
    def disable_jog(self):    
        # Disable Jog : All positionner must be idle (velocity = 0)
        [errorCode, returnString] = myxps.GroupJogModeDisable(socketId, group)
        if (errorCode != 0):
            displayErrorAndClose (socketId, errorCode, 'GroupJogModeDisable')
            sys.exit()
        else :
            print "GroupJogModeDisable %s sucessfull" % group
        
    
    #===============================================================================
    # # Make some moves
    # for index in range(10):
    #     # Forward
    #     [errorCode, returnString] = myxps.GroupMoveAbsolute(socketId, positioner, [40.0])
    #     if (errorCode != 0):
    #         displayErrorAndClose (socketId, errorCode, 'GroupMoveAbsolute')
    #         sys.exit()
    #     # Get current position
    #     [errorCode, currentPosition] = myxps.GroupPositionCurrentGet(socketId, positioner, 1)
    #     if (errorCode != 0):
    #         displayErrorAndClose (socketId, errorCode, 'GroupPositionCurrentGet')
    #         sys.exit()
    #     else:
    #         print 'Positioner ' + positioner + ' is in position ' + str(currentPosition)
    #     # Backward
    #     [errorCode, returnString] = myxps.GroupMoveAbsolute(socketId, positioner, [20.0])
    #     if (errorCode != 0):
    #         displayErrorAndClose (socketId, errorCode, 'GroupMoveAbsolute')
    #         sys.exit()
    #     # Get current position
    #     [errorCode, currentPosition] = myxps.GroupPositionCurrentGet(socketId, positioner, 1)
    #     if (errorCode != 0):
    #         displayErrorAndClose (socketId, errorCode, 'GroupPositionCurrentGet')
    #         sys.exit()
    #     else:
    #         print 'Positioner ' + positioner + ' is in position ' + str(currentPosition)
    #===============================================================================
    def close_connection(self):
        # Close connection
        myxps.TCP_CloseSocket(socketId)
    #----------- End of the demo program ----------#
    
#===============================================================================
# if __name__ == '__main__':
#     ctrl = DriversXPSQ()
#===============================================================================
        
