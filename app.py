# -*- coding: utf-8 -*-
"""
@author:team_13
"""

import sys
from PyQt5.QtWidgets import QMainWindow,QApplication, QWidget,QFileDialog, QMessageBox
from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import os
from vtk.util.misc import vtkGetDataRoot


mypath=r"C:\Users\user\Desktop\Head"
surfaceExtractor = vtk.vtkContourFilter()
volumeColor = vtk.vtkColorTransferFunction()
volumeScalarOpacity = vtk.vtkPiecewiseFunction()


def iso_slider(val):
    surfaceExtractor.SetValue(0, val)
    iren.update()

def sRed(val):
         sgreen=volumeColor.GetGreenValue (10)
         sblue=volumeColor.GetBlueValue (10)
         volumeColor.RemovePoint (10)
         volumeColor.AddRGBPoint(10, val/10 , sgreen , sblue)
         iren.update()
def sGreen(val):
         sred=volumeColor.GetRedValue (10)
         sblue=volumeColor.GetBlueValue (10)
         volumeColor.RemovePoint (10)
         volumeColor.AddRGBPoint(10, sred , val/10 , sblue)
         iren.update()
def sBlue(val):
         sred=volumeColor.GetRedValue (10)
         sgreen=volumeColor.GetGreenValue (10)
         volumeColor.RemovePoint (10)
         volumeColor.AddRGBPoint(10, sred , sgreen , val/10)
         iren.update()
def sOpacity(val):
         volumeScalarOpacity.RemovePoint (10)
         volumeScalarOpacity.AddPoint(10, val/100)
         iren.update()
def bRed(val):
         sgreen=volumeColor.GetGreenValue (2000)
         sblue=volumeColor.GetBlueValue (2000)
         volumeColor.RemovePoint (2000)
         volumeColor.AddRGBPoint(2000, val/10 , sgreen , sblue)
         iren.update()
def bGreen(val):
         bred=volumeColor.GetRedValue (2000)
         bblue=volumeColor.GetBlueValue (2000)
         volumeColor.RemovePoint (2000)
         volumeColor.AddRGBPoint(2000, bred ,val/10, bblue)
         iren.update()
def bBlue(val):
         bred=volumeColor.GetRedValue (2000)
         bgreen=volumeColor.GetGreenValue (2000)
         volumeColor.RemovePoint (2000)
         volumeColor.AddRGBPoint(2000, bred , bgreen , val/10)
         iren.update()
def bOpacity(val):
         volumeScalarOpacity.RemovePoint (2000)
         volumeScalarOpacity.AddPoint(2000, val/100)
         iren.update()
         

    
class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.horizontalSlider.valueChanged.connect(iso_slider)
        self.ui.horizontalSlider_2.valueChanged.connect(sRed)
        self.ui.horizontalSlider_3.valueChanged.connect(sGreen)
        self.ui.horizontalSlider_4.valueChanged.connect(sBlue)
        self.ui.horizontalSlider_5.valueChanged.connect(bRed)
        self.ui.horizontalSlider_6.valueChanged.connect(bGreen)
        self.ui.horizontalSlider_7.valueChanged.connect(bBlue)
        self.ui.horizontalSlider_8.valueChanged.connect(sOpacity)
        self.ui.horizontalSlider_9.valueChanged.connect(bOpacity)
        self.ui.Browse.clicked.connect(read_dcm)
        self.ui.sRender.clicked.connect(vtk_rendering)
        self.ui.vRender.clicked.connect(rayCasting)
        self.show()  
    


def read_dcm():
        fname = QtWidgets.QFileDialog.getExistingDirectory(None,"Open dcm's folder",os.path.expanduser("~"),QtWidgets.QFileDialog.ShowDirsOnly)
        msg = QMessageBox()
        msg.setWindowTitle("Info")
        msg.setText("CT Data Loaded Successfully!")
        if fname:
                msg.exec_()
                global mypath
                mypath=fname


def vtk_rendering(path):
        if mypath:
                path=mypath   
                renWin = iren.GetRenderWindow()
                aRenderer = vtk.vtkRenderer()
                renWin.AddRenderer(aRenderer)

                # Read Dataset using vtkDICOMImageReader 
                PathDicom =path
                reader = vtk.vtkDICOMImageReader()
                reader.SetDirectoryName(PathDicom)
                reader.Update()
        
                # An isosurface, or contour value of 500 is known to correspond to the
                surfaceExtractor.SetInputConnection(reader.GetOutputPort())
                surfaceExtractor.SetValue(0, 25)
                surfaceNormals = vtk.vtkPolyDataNormals()
                surfaceNormals.SetInputConnection(surfaceExtractor.GetOutputPort())
                surfaceNormals.SetFeatureAngle(60.0)
                surfaceMapper = vtk.vtkPolyDataMapper()
                surfaceMapper.SetInputConnection(surfaceNormals.GetOutputPort())
                surfaceMapper.ScalarVisibilityOff()
                surface = vtk.vtkActor()
                surface.SetMapper(surfaceMapper)
        
                aCamera = vtk.vtkCamera()
                aCamera.SetViewUp(0, 0, -1)
                aCamera.SetPosition(0, 1, 0)
                aCamera.SetFocalPoint(0, 0, 0)
                aCamera.ComputeViewPlaneNormal()
        
                aRenderer.AddActor(surface)
                aRenderer.SetActiveCamera(aCamera)
                aRenderer.ResetCamera()
        
                aRenderer.SetBackground(0, 0, 0)
        
                aRenderer.ResetCameraClippingRange()
        
                # Interact with the data.
                iren.Initialize()
                renWin.Render()
                iren.Start()
                iren.show()
        else:
                pass

def rayCasting(path):
        if mypath:
                path=mypath   
                renWin = iren.GetRenderWindow()
                ren = vtk.vtkRenderer()
                renWin.AddRenderer(ren)

                # Read Dataset using vtkDICOMImageReader 
                PathDicom =path
                reader = vtk.vtkDICOMImageReader()
                reader.SetDirectoryName(PathDicom)
                reader.Update()

                volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
                volumeMapper.SetInputConnection(reader.GetOutputPort())
                volumeMapper.SetBlendModeToComposite()

                # volumeColor = vtk.vtkColorTransferFunction()
                volumeColor.AddRGBPoint(0,    0.0, 0.0, 0.0)
                volumeColor.AddRGBPoint(10,  0.8, 0.3, 0.4)
                volumeColor.AddRGBPoint(2000, 0.0, 0.0, 1.0)
                volumeColor.AddRGBPoint(1150, 1.0, 1.0, 0.9)

                # volumeScalarOpacity = vtk.vtkPiecewiseFunction()
                volumeScalarOpacity.AddPoint(0,    0.00)
                volumeScalarOpacity.AddPoint(10,   1.0)
                volumeScalarOpacity.AddPoint(2000, 0.15)
                volumeScalarOpacity.AddPoint(1150, 0.85)

                volumeGradientOpacity = vtk.vtkPiecewiseFunction()
                volumeGradientOpacity.AddPoint(0,   0.0)
                volumeGradientOpacity.AddPoint(90,  0.5)
                volumeGradientOpacity.AddPoint(100, 0.0)

                volumeProperty = vtk.vtkVolumeProperty()
                volumeProperty.SetColor(volumeColor)
                volumeProperty.SetScalarOpacity(volumeScalarOpacity)
                volumeProperty.SetGradientOpacity(volumeGradientOpacity)
                volumeProperty.SetInterpolationTypeToLinear()
                volumeProperty.ShadeOn()
                volumeProperty.SetAmbient(0.4)
                volumeProperty.SetDiffuse(0.6)
                volumeProperty.SetSpecular(0.2)

                volume = vtk.vtkVolume()
                volume.SetMapper(volumeMapper)
                volume.SetProperty(volumeProperty)

                ren.AddViewProp(volume)

                camera =  ren.GetActiveCamera()
                c = volume.GetCenter()
                camera.SetFocalPoint(c[0], c[1], c[2])
                camera.SetPosition(c[0] + 400, c[1], c[2])
                camera.SetViewUp(0, 0, -1)

                renWin.SetSize(640, 480)

                iren.Initialize()
                renWin.Render()
                iren.Start()
                iren.show()
        else: 
                pass



app = QApplication(sys.argv)
# The class that connect Qt with VTK
iren = QVTKRenderWindowInteractor()
w = AppWindow()
#vtk_rendering()
w.show()
sys.exit(app.exec_())
# Start the event loop.
