# -*- coding: utf-8 -*-
#******************************************************************************
# Arenda Info
# ---------------------------------------------------------
# This plugin takes coordinates of a mouse click open information from http://geoportal.roslesinforg.ru:8080/arend_popup.php?
# This plugin is modified from Send2GoofleEath plugin by
# Copyright (C) 2013 Maxim Dubinin (sim@gis-lab.info), NextGIS (info@nextgis.org)
# Modified by igor Glushkov
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import arenda_tools

# initialize resources (icons) from resouces.py
import resources

class arenda_info:

  def __init__(self, iface):
    """Initialize class"""
    # save reference to QGIS interface
    self.iface = iface
    self.qgsVersion = unicode(QGis.QGIS_VERSION_INT)
  
  def initGui(self):
    """Initialize graphic user interface"""
    #check if the plugin is ran below 2.0
    if int(self.qgsVersion) < 10900:
        qgisVersion = self.qgsVersion[0] + "." + self.qgsVersion[2] + "." + self.qgsVersion[3]
        QMessageBox.warning(self.iface.mainWindow(),
                            "arenda_info", "Error",
                            "arenda_info", "QGIS %s detected.\n" % (qgisVersion) +
                            "arenda_info", "This version of TestPlugin requires at least QGIS version 2.0.\nPlugin will not be enabled.")
        return None

    #create action that will be run by the plugin
    self.action = QAction("Get arenda info", self.iface.mainWindow())
    self.action.setIcon(QIcon(":/icons/cursor.png"))
    self.action.setWhatsThis("Get arenda info")
    self.action.setStatusTip("Get coordinates of a mouse click and aplly request for arenda")
    
    # add plugin menu to Vector toolbar
    self.iface.addPluginToMenu("GetArendaInfo",self.action)
    
    # add icon to new menu item in Vector toolbar
    self.iface.addToolBarIcon(self.action)

    # connect action to the run method
    self.action.triggered.connect(self.run)

    # prepare map tool
    self.mapTool = arenda_tools.GetArendaInfo(self.iface)
    #self.iface.mapCanvas().mapToolSet.connect(self.mapToolChanged)
      
  def unload(self):
    """Actions to run when the plugin is unloaded"""
    # remove menu and icon from the menu
    self.iface.removeToolBarIcon(self.action)
    self.iface.removePluginMenu("SGet arenda info",self.action)

    if self.iface.mapCanvas().mapTool() == self.mapTool:
      self.iface.mapCanvas().unsetMapTool(self.mapTool)

    del self.mapTool

  def run(self):
    """Action to run"""
    # create a string and show it

    self.iface.mapCanvas().setMapTool(self.mapTool)
