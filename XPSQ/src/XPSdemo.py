'''
Created on 23 sept. 2015

@author: b.christol
'''
# --------- Python program: XPS controller demonstration -------- #
import sys

import XPS_Q8_drivers
from driver import *


#import time
# Display error function: simplify error print out and closes socket
def displayErrorAndClose (socketId, errorCode, APIName):
    if (errorCode != -2) and (errorCode != -108):
        [errorCode2, errorString] = myxps.ErrorStringGet(socketId, errorCode)
        if (errorCode2 != 0):
            print APIName + ': ERROR ' + str(errorCode)
        else:
            print APIName + ': ' + errorString
    else:
        if (errorCode == -2):
            print APIName + ': TCP timeout'
        if (errorCode == -108):
            print APIName + ': The TCP/IP connection was closed by an administrator'
    myxps.TCP_CloseSocket(socketId)
    return


# Instantiate the class
myxps = XPS_Q8_drivers.XPS()

ip = '192.168.0.201'
port = 5001

# Connect to the XPS
socketId = myxps.TCP_ConnectToServer(ip, port, 20)

# Check connection passed
if (socketId == -1):
    print 'Connection to XPS failed, check IP & Port'
    sys.exit()
else :
    print "Connexion at %s on %d successful, continue ..." % (ip, port)

# Add here your personal codes, below for example:
# Define the positioner
group = 'S1'
positioner = group + '.AXE_X'
# Kill the group
[errorCode, returnString] = myxps.GroupKill(socketId, group)
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode, 'GroupKill')
    sys.exit()
else :
    print "GroupKill %s sucessfull" % group

# Initialize the group
[errorCode, returnString] = myxps.GroupInitialize(socketId, group)
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode, 'GroupInitialize')
    sys.exit()
else :
    print "GroupInitialize %s sucessfull" % group
    
# Home search
[errorCode, returnString] = myxps.GroupHomeSearch(socketId, group)
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode, 'GroupHomeSearch')
    sys.exit()
else :
    print "GroupHomeSearch %s sucessfull" % group
        
# Enable Jog
[errorCode, returnString] = myxps.GroupJogModeEnable(socketId, group)
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode, 'GroupJogModeEnable')
    sys.exit()
else :
    print "GroupJogModeEnable %s sucessfull" % group
    
# Get JOG value
[errorCode, velocity, acceleration] = myxps.GroupJogParametersGet(socketId, group, 1)
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode, 'GroupJogParametersGet')
    sys.exit()
else :
    print "GroupJogParametersGet %s sucessfull" % group
    print "Velocity : %d" % velocity
    print "Acceleration : %d" % acceleration
   

velocity = [10]
acceleration = [5]

# Set JOG values
[errorCode, returnString] = myxps.GroupJogParametersSet(socketId, group, velocity, acceleration, 1)
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode, 'GroupJogParametersSet')
    sys.exit()
else :
    print "GroupJogParametersSet %s sucessfull" % group
    print "Velocity : %s" % velocity
    print "Acceleration : %s" % acceleration
     
     
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

# Abort group move
[errorCode, state] = myxps.GroupMoveAbort(socketId, group)
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode, 'GroupMoveAbort')
    sys.exit()
else :
    print "GroupMoveAbort %s sucessfull" % group
  
       
    
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
        
# Close connection
myxps.TCP_CloseSocket(socketId)
#----------- End of the demo program ----------#
