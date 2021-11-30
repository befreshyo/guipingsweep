#import wxversion
#wxversion.select("2.8")
import wx
import sys
#import ping
from ping3 import ping
import socket
from time import gmtime, strftime
from random import randint
from time import sleep

def pingScan(event):
        #check start host <= end host
        if hostEnd.GetValue() < hostStart.GetValue():
                dlg = wx.MessageDialog(mainWin,"Invalid Local Host Selection", "Confirm", wx.OK | wx.ICON_EXCLAMATION)
                result = dlg.ShowModal()
                dlg.Destroy()
                return
                
        #update the Status Bar
        mainWin.StatusBar.SetStatusText('Executing Ping Sweep .... Please Wait')
        
        #record the Start Time
        utcStart = gmtime()
        utc = strftime("%a, %d %b %Y %X +0000", utcStart)
        results.AppendText("\n\nPing Sweep Started: "+ utc+ "\n\n")

        #build the base IP address string
        baseIP = str(ipaRange.GetValue())+'.'+str(ipbRange.GetValue())+'.'+str(ipcRange.GetValue())+'.'
        ipRange = []
        for i in range(hostStart.GetValue(), (hostEnd.GetValue()+1)):
                ipRange.append(baseIP+str(i))

        #for each of the IP addresses, attempt an PING
        for ipAddress in ipRange:
                try:
                        #wait a random number of seconds, between 1 and 5, between each ping in the network range
                        if stealthMode.GetValue() == True:
                            sleep(randint(0,5))
                        #report the IP address to the window status bar
                        mainWin.StatusBar.SetStatusText('Pinging IP: '+ ipAddress)
                        #perform the ping
                        delay = ping(ipAddress, timeout=2)
                        #display the IP address in the main window
                        results.AppendText(ipAddress+'\t')
                        if delay != None:
                                #if successful (i.e. no timeout) display the result and response time 
                                results.AppendText('   Response Success')
                                results.AppendText('   Response Time: ' + str(delay) + ' Seconds')
                                results.AppendText("\n")
                        else :
                                #if delay == None, then the request timed out
                                results.AppendText('   Response Timeout')
                                results.AppendText("\n")      
                except socket.error as error:
                        # for socket errors report the offending IP
                        results.AppendText(ipAddress)
                        results.AppendText('   Response Failed: ') 
                        results.AppendText(error.message)
                        results.AppendText("\n")

        #record and display the ending time of the sweep
        utcEnd = gmtime()
        utc = strftime("%a, %d %b %Y %X +0000", utcEnd)
        results.AppendText("\nPing Sweep Ended: "+ utc + "\n\n")    

        #clear the status bar
        mainWin.StatusBar.SetStatusText('')
        return

#exit program
def programExit(event):
        sys.exit()
        
#setup application window
app = wx.App()

# define window
mainWin = wx.Frame(None, title="Simple Ping (ICMP) Sweeper 1.0", size =(1000,600))

#define the action panel
panelAction = wx.Panel(mainWin)

#define action buttons
stealthMode = wx.CheckBox(panelAction, -1, 'Stealth Mode', (10, 10))
stealthMode.SetValue(False)

#scan button
scanButton = wx.Button(panelAction, label='Scan')
scanButton.Bind(wx.EVT_BUTTON, pingScan)

#exit button
exitButton  = wx.Button(panelAction, label='Exit')
exitButton.Bind(wx.EVT_BUTTON, programExit)

# define a text area to display results
results = wx.TextCtrl(panelAction, style = wx.TE_MULTILINE | wx.HSCROLL)

#base network for class c IP addresses has 3 components for class c addresses, the first 3 octets define the network i.e 127.0.0
#the last 8 bits define the host i.e. 0-255 3 spin controls one for each of the 4 network octets + set the default value to 127.0.0.0 for convienence
ipaRange = wx.SpinCtrl(panelAction, -1, '')
ipaRange.SetRange(0, 255)
ipaRange.SetValue(127)

ipbRange = wx.SpinCtrl(panelAction, -1, '')
ipbRange.SetRange(0, 255)
ipbRange.SetValue(0)

ipcRange = wx.SpinCtrl(panelAction, -1, '')
ipcRange.SetRange(0, 255)
ipcRange.SetValue(0)

#add a lable for the user 
ipLabel = wx.StaticText(panelAction, label="IP Base: ")

#user has the ability to set the port range they wish to scan (maximum is 0-255)
hostStart = wx.SpinCtrl(panelAction, -1, '')
hostStart.SetRange(0, 255)
hostStart.SetValue(1)

hostEnd = wx.SpinCtrl(panelAction, -1, '')
hostEnd.SetRange(0, 255)
hostEnd.SetValue(10)

HostStartLabel = wx.StaticText(panelAction, label="Host Start: ")
HostEndLabel = wx.StaticText(panelAction, label="Host End: ")

#create BoxSizer to automatically align the different components neatly, create a horizontal Box, add the buttons, ip range and host spin controls
actionBox = wx.BoxSizer()
actionBox.Add(scanButton, proportion=1, flag=wx.LEFT, border=5)
actionBox.Add(exitButton, proportion=0, flag=wx.LEFT, border=5)


actionBox.Add(stealthMode, proportion=0,  flag=wx.LEFT|wx.CENTER,  border=5)

actionBox.Add(ipLabel, proportion=0, flag=wx.LEFT, border=5)

actionBox.Add(ipaRange, proportion=0, flag=wx.LEFT, border=5)
actionBox.Add(ipbRange, proportion=0, flag=wx.LEFT, border=5)
actionBox.Add(ipcRange, proportion=0, flag=wx.LEFT, border=5)

actionBox.Add(HostStartLabel, proportion=0, flag=wx.LEFT|wx.CENTER, border=5)
actionBox.Add(hostStart, proportion=0, flag=wx.LEFT, border=5)

actionBox.Add(HostEndLabel, proportion=0, flag=wx.LEFT|wx.CENTER, border=5)
actionBox.Add(hostEnd, proportion=0, flag=wx.LEFT, border=5)

#create a Vertical Box that places the horizontal box inside along with the results text area
vertBox = wx.BoxSizer(wx.VERTICAL)
vertBox.Add(actionBox, proportion=0, flag=wx.EXPAND | wx.ALL, border = 5)
vertBox.Add(results, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

#adding a menu and status bar to the main window
mainWin.CreateStatusBar()

#SetSizer function automatically size the windows based on the the definitions above
panelAction.SetSizer(vertBox)

# make the program relayout everything after all controls are added
panelAction.Layout()

#display the main window 
mainWin.Show()

#enter the applications main loop, awaiting user actions
app.MainLoop()
