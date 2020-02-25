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
from qgis.gui import *

import resources
import os
import tempfile
import platform
import subprocess
import webbrowser
#main class
class GetArendaInfo(QgsMapTool):
  def __init__(self, iface):
    QgsMapTool.__init__(self, iface.mapCanvas())

    self.canvas = iface.mapCanvas()
    #self.emitPoint = QgsMapToolEmitPoint(self.canvas)
    self.iface = iface

    self.cursor = QCursor(QPixmap(':/icons/cursor.png'), 1, 1)

  def activate(self):
    self.canvas.setCursor(self.cursor)
  
  def canvasReleaseEvent(self, event):

    QApplication.setOverrideCursor(Qt.WaitCursor)
    x = event.pos().x()
    y = event.pos().y()
    point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
    QApplication.restoreOverrideCursor()
    
    
    crsSrc = self.canvas.mapRenderer().destinationCrs()
    crsWGS = QgsCoordinateReferenceSystem(4326)
    
    if crsSrc.authid() != "4326":
        xform = QgsCoordinateTransform(crsSrc, crsWGS)
        point = xform.transform(QgsPoint(point.x(),point.y()))
    
    url='http://geoportal.roslesinforg.ru:8080/arend_popup.php?x=%s&y=%s'%(str(point.x()),str(point.y()))
    #winpath = 'C:/Program Files/Google/Google Earth/client/googleearth.exe'
    #if not os.path.exists(winpath): winpath = 'C:/Program Files (x86)/Google/Google Earth/client/googleearth.exe'
    
    #linpath = 'google-earth'
    #linpath_debian = 'googleearth'
    
    unknown = False
    ret = 0
    
    if platform.system() == 'Windows':
      #cmd = "start /B " + "\"" + winpath + "\" "+ f.name
      #ret = os.system(cmd)
      if event.modifiers() == Qt.ShiftModifier:
        #subprocess.Popen([winpath, f.name])
        webbrowser.open(url, new=0, autoraise=False)
      else:
        webbrowser.open(url, new=0, autoraise=False)
    elif platform.system() == 'Linux':
      webbrowser.open(url, new=0, autoraise=False)      
    elif platform.system() == "Darwin":
      ret = webbrowser.open(url, new=0, autoraise=False)
    else:
      unknown = True

    if unknown == True:
      QMessageBox.warning(self.canvas,'Error','Unknown operation system. Please let developers of the plugin know.')
    if ret != 0:
      QMessageBox.warning(self.canvas,'Error','Unable to send to GE, executable not found.\n I tried ' + linpath)
    
    #os.unlink(f.name)
