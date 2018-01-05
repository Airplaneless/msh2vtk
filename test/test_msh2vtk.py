import vtk
import unittest
from module import MSH2VTK

GMSH_PATH = '/opt/onelab-Linux64/gmsh'

class Test(unittest.TestCase):
    def test(self):
        converter = MSH2VTK(GMSH_PATH, 'cubic.msh')
        ugrid = converter.convert()
        self.assertEqual(bool(ugrid), True)

        writer = vtk.vtkUnstructuredGridWriter()
        writer.SetInputData(ugrid)
        writer.SetFileName('cubic.vtk')
        writer.Write()