"""!
@package wmsmenu.py

@brief Main python app for handling wms requests for getCapabilities
and getMaps.  

Classes:
 - wmsFrame
Functions:
 - DisplayWMSMenu
 
(C) 2006-2011 by the GRASS Development Team
This program is free software under the GNU General Public
License (>=v2). Read the file COPYING that comes with GRASS
for details.

@author: Maris Nartiss (maris.nartiss gmail.com)
@author Sudeep Singh Walia (Indian Institute of Technology, Kharagpur , sudeep495@gmail.com)
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon Jul 11 04:58:20 2011

import wx
from wxPython.wx import *
from grass.script import core as grass
import imghdr
from wx.lib.pubsub import Publisher
from urllib2 import Request, urlopen, URLError, HTTPError
from parse import *
from WMSMapDisplay import NewImageFrame
from addserver import AddServerFrame
from ServerInfoAPIs import addServerInfo, removeServerInfo, updateServerInfo, initServerInfoBase, getAllRows
from LoadConfig import loadConfigFile


# begin wxGlade: extracode
# end wxGlade

class LayerData():
    name = None
    title = None
    abstract = None
    srs = None
    
    def printLayerData(self,layerDataDict):
        for key, value in layerDataDict.iteritems():
            print key
            print value.name
            print value.title
            print value.abstract
            srss = value.srs
            for srs in srss:
                a = srs.string
                a = a.split(':')
                print a[0]+' '+a[1]
            print '--------------------------------------------'
            
    def appendLayerTree(self, layerDataDict, LayerTree, layerTreeRoot):
        for key, value in layerDataDict.iteritems():
            name = value.name
            title = value.title
            abstract = value.abstract
            string = str(key)+"-"+name+":"+title+":"+abstract
            LayerTree.AppendItem(layerTreeRoot, string)
    
    def setKeyToEPSGCodes(self, layerDataDict):
        keytoepsgcodes = {}
        for key, value in layerDataDict.iteritems():
            srss = value.srs
            l=[]
            for srs in srss:
                a = srs.string
                a = a.split(':')
                l = l+[a[1]]
            print 'here'
            print 'key = ' + str(key) 
            print l
            print 'now'
            keytoepsgcodes[str(key)] = l
            
            print 'dict value now is '
            print keytoepsgcodes
            print 'dict printed'
        
        print 'final dict'
        print keytoepsgcodes
        print 'final dcit printed'
        return keytoepsgcodes

class Message():
    pass

class wmsFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wmsFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.StatusBar = self.CreateStatusBar(1, 0)
        self.URL = wx.StaticText(self, -1, "URL")
        self.ServerList = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_SIMPLE)
        self.LayerTree = wx.TreeCtrl(self, -1, style=wx.TR_HAS_BUTTONS|wx.TR_NO_LINES|wx.TR_MULTIPLE|wx.TR_MULTIPLE|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER)
        self.username = wx.StaticText(self, -1, "UserName")
        self.usernameInput = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_TAB)
        self.EPSG = wx.StaticText(self, -1, "EPSG")
        self.password = wx.StaticText(self, -1, "Password")
        self.passwordInput = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_TAB|wx.TE_PASSWORD)
        self.epsgList = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_SIMPLE|wx.CB_DROPDOWN)
        self.GetCapabilities = wx.Button(self, -1, "GetCapabilities")
        self.GetMaps = wx.Button(self, -1, "GetMaps")
        self.addServer = wx.Button(self, -1, "Manage Servers")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT_ENTER, self.OnServerListEnter, self.ServerList)
        self.Bind(wx.EVT_COMBOBOX, self.OnServerList, self.ServerList)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnLayerTreeSelChanged, self.LayerTree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnLayerTreeActivated, self.LayerTree)
        self.Bind(wx.EVT_BUTTON, self.OnGetCapabilities, self.GetCapabilities)
        self.Bind(wx.EVT_BUTTON, self.OnGetMaps, self.GetMaps)
        self.Bind(wx.EVT_BUTTON, self.OnAddServer, self.addServer)
        # end wxGlade
        
        #Sudeep's Code Starts
        #self.urlInput.SetValue('http://www.gisnet.lv/cgi-bin/topo')
        self.usernameInput.Disable()
        self.passwordInput.Disable()
        print 'new version'
        if( not loadConfigFile(self)):
            print 'Config File Error, Unable to start application...'
            grass.fatal_error('Config File Error, Unable to start application...')
            self.Close()
            return

        self.soup, open = initServerInfoBase('ServersList.xml')
        if(not open):
            self.Close()
            return
        self.__populate_Url_List(self.ServerList)
        self.selectedURL="No server selected"
        self.layerTreeRoot = self.LayerTree.AddRoot("Layers")
        Publisher().subscribe(self.onAddServerFrameClose, ("Add_Server_Frame_Closed"))
        Publisher().subscribe(self.onUpdateServerListmessage, ("update.serverList"))
        Publisher().subscribe(self.onUpdateMapListmessage, ("update.map_servernameTouid"))
        
        self.keyToEPSGCodes = {}
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.AddServerisClosed = True
        self.layerName = ""
        
        #items = ["a", "b", "c"]
        #itemId = self.LayerTree.AppendItem(self.layerTreeRoot, "item")
        #self.LayerTree.AppendItem(itemId, "inside")
        #Sudeep's Code Ends 
    def __set_properties(self):
        # begin wxGlade: wmsFrame.__set_properties
        self.SetTitle("wmsFrame")
        self.StatusBar.SetStatusWidths([-1])
        # statusbar fields
        StatusBar_fields = ["StatusBar"]
        for i in range(len(StatusBar_fields)):
            self.StatusBar.SetStatusText(StatusBar_fields[i], i)
        self.LayerTree.SetMinSize((400, 250))
        self.usernameInput.SetMinSize((189, 27))
        self.passwordInput.SetMinSize((189, 27))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wmsFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.FlexGridSizer(2, 3, 1, 1)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(self.URL, 0, 0, 0)
        sizer_3.Add(self.ServerList, 0, 0, 0)
        sizer_2.Add(sizer_3, 0, 0, 0)
        sizer_2.Add(self.LayerTree, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.username, 0, 0, 0)
        grid_sizer_1.Add(self.usernameInput, 0, 0, 0)
        grid_sizer_1.Add(self.EPSG, 0, 0, 0)
        grid_sizer_1.Add(self.password, 0, 0, 0)
        grid_sizer_1.Add(self.passwordInput, 0, 0, 0)
        grid_sizer_1.Add(self.epsgList, 0, 0, 0)
        sizer_2.Add(grid_sizer_1, 0, wx.EXPAND, 0)
        sizer_4.Add(self.GetCapabilities, 0, 0, 0)
        sizer_4.Add(self.GetMaps, 0, 0, 0)
        sizer_4.Add(self.addServer, 0, 0, 0)
        sizer_2.Add(sizer_4, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_1.Add(sizer_2, 1, wx.ALL|wx.EXPAND|wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.SHAPED, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade
    

    def OnGetCapabilities(self, event): # wxGlade: wmsFrame.<event_handler>            
        ''''f=open('check.xml','r')
        xml=f.read()
        f.close()
        layerDataDict = parsexml2(xml)
        ld = LayerData()
        #ld.printLayerData(layerDataDict)
        ld.appendLayerTree(layerDataDict, self.LayerTree, self.layerTreeRoot)
        self.LayerTree.Expand(self.layerTreeRoot)
        return'''
        if(self.selectedURL == "No server selected"):
            message = 'No Server selected'
            self.ShowMessage(message, 'Warning')
            StatusBar_fields = [message]
            self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
            grass.warning(message)
            print message
            return
        
        self.usernameInput.Enable()
        self.passwordInput.Enable()
        #Sudeep's Code Starts
        #url = 'http://www.gisnet.lv/cgi-bin/topo?request=GetCapabilities&service=wms&version=1.1.1'
        self.LayerTree.CollapseAndReset(self.layerTreeRoot)
        #url = self.urlInput.GetValue() 
        url = self.selectedURL
        url = url + '?request=GetCapabilities&service=wms&version=1.1.1'
        print url
        StatusBar_fields = ["GetCapabilities Request Sent..."]
        self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
        req = Request(url)
        try:
            response = urlopen(req, None, self.timeoutValueSeconds)
            xml = response.read()
            if(not isValidResponse(xml)):
                message = "Invalid GetCapabilities response"
                self.ShowMessage(message, 'Warning')
                StatusBar_fields = [message]
                self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
                grass.warning(message)
                print message
                return
            if(isServiceException(xml)):
                message = 'Service Exception in Get Capabilities'
                self.ShowMessage(message, 'Warning')
                StatusBar_fields = [message]
                self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
                grass.warning(message)
                print message                
                return
            #for testing pruposes
            #f=open('in1.xml','r')
            #xml=f.read()
            #f.close()
            #self.statusbar.SetStatusText(xml) 
            #reslist = parsexml(xml)
            #populateLayerTree(xml,self.LayerTree, self.layerTreeRoot)
            print 'check1'
            layerDataDict = parsexml2(xml)
            print 'check2'
            ld = LayerData()
            print 'check3'
            #ld.printLayerData(layerDataDict)
            ld.appendLayerTree(layerDataDict, self.LayerTree, self.layerTreeRoot)
            self.keyToEPSGCodes = ld.setKeyToEPSGCodes(layerDataDict)
            print self.keyToEPSGCodes
            print 'check4'
            #for res in reslist:
            #       self.LayerTree.AppendItem(self.layerTreeRoot, res)
            #self.Layers.SetValue(st) 
            #print xml
            self.LayerTree.Expand(self.layerTreeRoot)
        except HTTPError, e:
            message = 'The server couldn\'t fulfill the request.'
            print message
            #print 'Error code: ', e.code
        except URLError, e: 
            message = 'Failed to reach a server.'
            print message
            #print 'Reason: ', e.reason
        except ValueError, e:
            message = 'Value error'
            print message
            #print 'Reason: ', e.reason
        except Exception, e:
            message = 'urlopen exception, unable to fetch data for getcapabilities'
            message = str(e)
            print 'printing exception here'
            print message
            print 'done'
        else:
            message = 'Successful'
            print message
            
        if(not message=='Successful'):
                self.ShowMessage(message, 'Warning')
                StatusBar_fields = [message]
                self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
                grass.warning(message)
        else:
            StatusBar_fields = [message]
            self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
            grass.message(message)
            #Sudeep's Code Ends
        event.Skip()
        
    
    def OnGetMaps(self, event): # wxGlade: wmsFrame.<event_handler>
        #Sudeep's Code Starts
        #self.layerName = self.layerSelected.GetValue()
        #url = self.urlInput.GetValue()
        print self.selectedURL
        if(self.selectedURL == "No server selected"):
            message = 'No server selected'
            print message
            grass.warning(message)
            self.ShowMessage(message, 'Warning')
            StatusBar_fields = [message]
            self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
            return
            
        
        self.url_in = self.selectedURL
        getMap_request_url = self.url_in
        getMap_request_url += '?service=WMS&request=GetMap&version=1.1.1&format=image/png&width=800&height=600&srs=EPSG:3059&layers='
        getMap_request_url += self.layerName+'&bbox=584344,397868,585500,398500'
        
        print getMap_request_url
    
        req = Request(getMap_request_url)
        try:
            
            message = 'GetMaps request sent. Waiting for response...'
            StatusBar_fields = [message]
            self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
            response = urlopen(req, None, self.timeoutValueSeconds)
            image = response.read()
            #print image
            
            if(isServiceException(image)):
                message = 'Service Exception has occured'
                self.ShowMessage(message, 'Warning')
                print message
                grass.warning(message)
                StatusBar_fields = [message]
                self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
            else:
                TMP = grass.tempfile()
                if TMP is None:
                    grass.fatal("Unable to create temporary files")
                print TMP
                
                outfile = open(TMP,'wb')
                outfile.write(image)
                outfile.close()
                if(imghdr.what(TMP) != 'png'):
                    #print 'uiui'
                    #print imghdr.what('./map.png')
                    message = 'Not a valid PNG Image, Unable to display Map'
                    self.ShowMessage(message, 'Warning')
                    print message
                    grass.warning(message)
                    StatusBar_fields = [message]
                    self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
                    return
                message = 'GetMap response obtained'
                grass.message(message)
                StatusBar_fields = [message]
                self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
                NewImageFrame(TMP)
            
            
        except HTTPError, e:
            message = 'The server couldn\'t fulfill the request.'
            print message
            #print 'Error code: ', e.code
        except URLError, e: 
            message = 'Failed to reach a server.'
            print message
            #print 'Reason: ', e.reason
        except ValueError, e:
            message = 'Value error'
            print message
            #print 'Reason: ', e.reason
        except:
            message = 'urlopen exception, unable to fetch data for getcapabilities'
            print message
        else:
            message = 'Successful'
            print message
                   
        print message
        if(message != 'Successful'):
            self.ShowMessage(message, 'Warning')
            grass.warning(message)
            StatusBar_fields = [message]
            self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
        else:
            grass.message(message)
            StatusBar_fields = [message]
            self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
        
        #Sudeep's Code Ends
        event.Skip()

    
    def OnServerListEnter(self, event): # wxGlade: wmsFrame.<event_handler>
        return
        '''
        print "Event handler `OnServerListEnter' not implemented"
        #Sudeep's Code Starts
        print self.ServerList.CurrentSelection
        newUrl = self.ServerList.GetValue()
        self.ServerList.Append(newUrl)
        
        url = newUrl.split()
        if(len(url)==2):
            self.servers[url[0]] = url[1]
            f = open('serverList.txt','a')
            f.write(newUrl+"\n")
            f.close()
            self.selectedURL = url[1]
            print self.selectedURL
            print self.servers
  
        else:
            print "Format not recognized, Format: Severname URL"
        #Sudeep's Code Ends
        event.Skip()
        '''
    
        
    def OnServerList(self, event): # wxGlade: wmsFrame.<event_handler>
        print "Event handler `OnServerList' not implemented"
        #Sudeep's Code Starts
        print self.ServerList.CurrentSelection
        info = self.ServerList.GetValue()
        if(len(info) == 0):
            return
        urlarr = info.split(self.name_url_delimiter)
        print "OnServerList:printing urlarr"
        print urlarr
        print urlarr[0]
        #print urlarr[0].encode()
        #self.printDict(self.servers)
        print "OnServerList: done"
        if(len(urlarr)==2):
            try:
            	uid = self.map_servernameTouid[urlarr[0]]
            	self.selectedURL = self.servers[uid].url
            	print self.selectedURL
            except KeyError,e:
                print e
            	message = 'key error reported'
                print message
            	print self.map_servernameTouid
                grass.warning(message)
        else:
            message = "Wrong format of URL selected"
            print message
            grass.warning(message)
        #Sudeep's Code Ends
        event.Skip()

    def OnLayerTreeActivated(self, event): # wxGlade: wmsFrame.<event_handler>
        #Sudeep's Code Starts
        print "OnLayerTreeActivated: ", self.LayerTree.GetItemText(event.GetItem())
        #Sudeep's Code Ends
        print "Event handler `OnLayerTreeActivated' not implemented"
        event.Skip()

    def OnLayerTreeSelChanged(self, event): # wxGlade: wmsFrame.<event_handler>
        #self.layerName = self.LayerTree.GetItemText(event.GetItem())
        #print "Event handler `OnLayerTreeSelChanged' not implemented"
        self.selectedLayerList = []
        keys =[]
        self.layerName = ""
        print "Selected layers:"
        for sellayer in self.LayerTree.GetSelections():
            layerNameString = self.LayerTree.GetItemText(sellayer)
            print 'here'
            print layerNameString
            layerNameStringList = layerNameString.split(':')
            print layerNameStringList
            print len(layerNameStringList)
            if(len(layerNameStringList)==0):
                message = 'Unable to select layers'
                self.ShowMessage(message, 'Warning')
                grass.warning(message)
                StatusBar_fields = [message]
                self.StatusBar.SetStatusText(StatusBar_fields[0], 0)
                return
            layerName = layerNameStringList[0].split('-')[1]
            key = layerNameStringList[0].split('-')[0]
            print layerName
            print 'done'
            self.selectedLayerList += [layerName]
            self.layerName += ","+layerName
            keys += [key]
          
          
        self.layerName = self.layerName[1:]
        print self.layerName
        self.epsgList.Clear()
        print self.keyToEPSGCodes
        for key in keys:
            lEPSG = self.keyToEPSGCodes[key]
            self.epsgList.AppendItems(lEPSG)
                
        #print "Event handler `OnLayerTreeSelChanged' not implemented"
        event.Skip()
        
    def OnAddServer(self, event): # wxGlade: wmsFrame.<event_handler>
        print 'before add server call'
        self.AddServerisClosed = False
        self.addServer.Disable()
        AddServerFrame(self)
        #print 'after add server call'
        #print "Event handler `OnAddServer' not implemented"
        #event.Skip()
        return 
    

    def onAddServerFrameClose(self, msg):
        self.AddServerisClosed = True
        self.addServer.Enable()
        #frame = self.GetParent()
        #frame.Show()
    
    def onUpdateServerListmessage(self, msg):
        #patch5s
        self.servers = msg.data
        print 'in update serverlistmessage()'
        print 'printing serverlist'
        self.printDict(self.servers)
        #patch5e
        self.__update_Url_List(self.ServerList)
        
        #patch5s
    def onUpdateMapListmessage(self, msg):
        print 'in update maplistmessage()' 
        self.map_servernameTouid = msg.data
        print 'printing map_servernametouid'
        self.printDict(self.map_servernameTouid)
        #patch5e
        
    def OnQuit(self, event):
        msg = ""
        print 'in quit'
        if(not self.AddServerisClosed):
            Publisher().sendMessage(("WMS_Menu_Close"), msg)
        self.Destroy()
        return
    
    def ShowMessage(self, message, type = 'Warning'):
        wx.MessageBox(message, type)
    
    def __update_Url_List(self, ComboBox):
        ComboBox.Clear()
        ComboBox.Append("")
        for key, value in self.servers.items():
            #string = '{0}{1}{2}'.format(value.servername,self.name_url_delimiter,value.url[0:self.urlLength])
            #ComboBox.Append(string)
            ComboBox.Append(value.servername+self.name_url_delimiter+value.url[0:self.urlLength])
            #ComboBox.Append(value.servername+" "+self.name_url_delimiter+" "+value.url)
        #print self.servers
        return
        
    def __populate_Url_List(self, ComboBox):
        self.servers, self.map_servernameTouid = getAllRows(self.soup)
        ComboBox.Append("")
        for key, value in self.servers.items():
            #string = '{0}{1}{2}'.format(value.servername,self.name_url_delimiter,value.url[0:self.urlLength])
            #ComboBox.Append(string)
            ComboBox.Append(value.servername+self.name_url_delimiter+value.url[0:self.urlLength])
            #ComboBox.Append(value.servername+" "+self.name_url_delimiter+" "+value.url)
        #print self.servers
        return
    
    
        '''f = open('serverList.txt','r')
        lines = f.readlines()
        self.servers = {}
        for line in lines:
            row = line.split()
            print row
            if(len(row) == 4) :
                self.servers[row[0]] = row[1]
            name = row[0]+" "+row[1][7:45]
            ComboBox.Append(name)
        f.close()'''

    def printDict(self,dict):
        for key in dict.keys():
            print "the key name is" + key + "and its value is" 
    

# end of class wmsFrame

#Sudeep's Code Starts
def DisplayWMSMenu():
        print 'DisplayWMSMenu loaded...'
        app = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        wms_Frame = wmsFrame(None, -1, "")
        app.SetTopWindow(wms_Frame)
        wms_Frame.Show()
        app.MainLoop()
#Sudeep's Code Ends

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    wms_Frame = wmsFrame(None, -1, "")
    app.SetTopWindow(wms_Frame)
    wms_Frame.Show()
    app.MainLoop()
