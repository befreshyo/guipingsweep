#import wxversion
#wxversion.select("2.8")
import wx
import sys
#import ping 
from ping3 import ping
from socket import *
from time import gmtime, strftime


def portScan(event):
        #check starting port <= ending port
        if portEnd.GetValue() < portStart.GetValue():
                dlg = wx.MessageDialog(mainWin,"Invalid Host Port Selection", "Confirm", wx.OK | wx.ICON_EXCLAMATION)
                result = dlg.ShowModal()
                dlg.Destroy()
                return
                
        #update status
        mainWin.StatusBar.SetStatusText('Executing Port Scan .... Please Wait')
        
        #record start time
        utcStart = gmtime()
        utc = strftime("%a, %d %b %Y %X +0000", utcStart)
        results.AppendText("\n\nPort Scan Started: "+ utc+ "\n\n")

        #build the base IP address string
        baseIP = str(ipaRange.GetValue())+'.'+str(ipbRange.GetValue())+'.'+str(ipcRange.GetValue())+'.'+str(ipdRange.GetValue())

        # for IP addresses specified scan the ports specified
        for port in range(portStart.GetValue(), portEnd.GetValue()+1):
                try:
                        #report the IP address to the window status bar
                        mainWin.StatusBar.SetStatusText('Scanning: '+ baseIP+' Port: '+str(port))
                        # open a socket
                        reqSocket = socket(AF_INET, SOCK_STREAM)
                        #try connecting to the specified IP, port
                        response = reqSocket.connect_ex((baseIP, port))
                        if(response == 0) :
                                #display the ipAddress and port
                                results.AppendText(baseIP+'\t'+str(port)+'\t')                                
                                results.AppendText('Open')
                                results.AppendText("\n")
                        else:
                                if displayAll.GetValue() == True:
                                        results.AppendText(baseIP+'\t'+str(port)+'\t')           
                                        results.AppendText('Closed')            
                                        results.AppendText("\n")
                        reqSocket.close()                        
                except socket.error as error:
                        # for socket errors report the offending IP
                        results.AppendText(baseIP+'\t'+str(port)+'\t')
                        results.AppendText('Failed: ') 
                        results.AppendText(error.message)
                        results.AppendText("\n")
        #record and display the ending time of the sweep
        utcEnd = gmtime()
        utc = strftime("%a, %d %b %Y %X +0000", utcEnd)
        results.AppendText("\nPort Scan Ended: "+ utc + "\n\n")    
        #clear the status bar
        mainWin.StatusBar.SetStatusText('')

#exit program
def programExit(event):
        sys.exit()

#setup application window
app = wx.App()

# define window
mainWin = wx.Frame(None, title="Simple Port Scanner", size =(1200,600))

#define the action panel
panelAction = wx.Panel(mainWin)

#define action buttons
displayAll = wx.CheckBox(panelAction, -1, 'Display All', (10, 10))
displayAll.SetValue(True)

stealthMode = wx.CheckBox(panelAction, -1, 'Stealth Mode', (10, 10))
stealthMode.SetValue(True)

#scan button
scanButton = wx.Button(panelAction, label='Scan')
scanButton.Bind(wx.EVT_BUTTON, portScan)

#exit button
exitButton  = wx.Button(panelAction, label='Exit')
exitButton.Bind(wx.EVT_BUTTON, programExit)

# define a text area to display results
results = wx.TextCtrl(panelAction, style = wx.TE_MULTILINE | wx.HSCROLL)

#base network for class c IP addresses has 3 components for class c addresses, the first 3 octets define the network i.e 127.0.0
#the last 8 bits define the host i.e. 0-255 3 spin controls one for each of the 4 network octets + set the default value to 127.0.0.0 for convienence
ipaRange     = wx.SpinCtrl(panelAction, -1, '')
ipaRange.SetRange(0, 255)
ipaRange.SetValue(127)

ipbRange = wx.SpinCtrl(panelAction, -1, '')
ipbRange.SetRange(0, 255)
ipbRange.SetValue(0)

ipcRange = wx.SpinCtrl(panelAction, -1, '')
ipcRange.SetRange(0, 255)
ipcRange.SetValue(0)

ipdRange = wx.SpinCtrl(panelAction, -1, '')
ipdRange.SetRange(0, 255)
ipdRange.SetValue(1)

#adding a lable for the user 
ipLabel = wx.StaticText(panelAction, label="IP Address: ")

#user has the ability to set the port range they wish to scan (maximum is 20-1025)
portStart = wx.SpinCtrl(panelAction, -1, '')
portStart.SetRange(1, 1025)
portStart.SetValue(1)

portEnd = wx.SpinCtrl(panelAction, -1, '')
portEnd.SetRange(1, 1025)
portEnd.SetValue(5)

PortStartLabel = wx.StaticText(panelAction, label="Port Start: ")
PortEndLabel = wx.StaticText(panelAction, label="Port  End: ")

#create BoxSizer to automatically align the different components neatly, create a horizontal Box, add the buttons, ip range and host spin controls
actionBox = wx.BoxSizer()

actionBox.Add(displayAll, proportion=0,  flag=wx.LEFT|wx.CENTER,  border=5)
actionBox.Add(stealthMode, proportion=0,  flag=wx.LEFT|wx.CENTER,  border=5)
actionBox.Add(scanButton, proportion=0,  flag=wx.LEFT,  border=5)
actionBox.Add(exitButton, proportion=0,  flag=wx.LEFT,  border=5)

actionBox.Add(ipLabel, proportion=0, flag=wx.LEFT|wx.CENTER, border=5)

actionBox.Add(ipaRange, proportion=0, flag=wx.LEFT, border=5)
actionBox.Add(ipbRange, proportion=0, flag=wx.LEFT, border=5)
actionBox.Add(ipcRange, proportion=0, flag=wx.LEFT, border=5)
actionBox.Add(ipdRange, proportion=0, flag=wx.LEFT, border=5)

actionBox.Add(PortStartLabel, proportion=0, flag=wx.LEFT|wx.CENTER, border=5)
actionBox.Add(portStart, proportion=0, flag=wx.LEFT, border=5)

actionBox.Add(PortEndLabel, proportion=0, flag=wx.LEFT|wx.CENTER, border=5)
actionBox.Add(portEnd, proportion=0, flag=wx.LEFT, border=5)

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