import vtk
import os
import re
import numpy as np
from vtk.util import numpy_support


class MSH2VTK:
    """
    Convert .msh to .vtk with saving physical groups
    """
    def __init__(self, gmsh_path, path):
        """
        Constructor for MSH2VTK
        :param gmsh_path: str
        Path to GMSH
        :param path: str
        Path to .msh file
        """
        self.gmsh_path = gmsh_path
        self.path = path

    def convert(self):
        """
        Convert to .vtk from .msh
        :return: vtkUnstructedGrid
        Refined vtk file
        """
        phys_group_dict = dict()
        phys_group_list = list()
        data = dict()

        kfv = lambda d, v: d.keys()[d.values().index(v)]

        os.system("{0} {1} -3 -format vtk > /dev/null".format(self.gmsh_path, self.path))

        reader_vtk = vtk.vtkUnstructuredGridReader()
        reader_vtk.SetFileName(self.path[:-4]+'.vtk')
        reader_vtk.Update()

        meshgrid = reader_vtk.GetOutput()
        # Reading phys. names and corresponding numbers
        with open(self.path[:-4] + '.msh', mode='r') as _file:
            line = _file.next()
            while True:
                if line == '$PhysicalNames\n':
                    break
                line = _file.next()
            _file.next()
            while True:
                line = _file.next()
                if line == '$EndPhysicalNames\n':
                    break
                ls = re.findall("[\w']+", line)
                phys_group_dict[int(ls[1])] = ls[2]
                phys_group_list.append(ls[2])
        # Zero numpy array
        for i in xrange(len(phys_group_list)):
            physname = phys_group_list[i]
            data[kfv(phys_group_dict, physname)] = np.zeros(meshgrid.GetNumberOfCells())
        # Reading elements and making list for elements, where
        # with 0 and 1 for physgroup
        with open(self.path[:-4] + '.msh', mode='r') as _file:
            line = _file.next()
            while True:
                if line == '$Elements\n':
                    break
                line = _file.next()
            _file.next()
            while True:
                line = _file.next()
                if line == '$EndElements\n':
                    break
                ls = re.findall("[\w']+", line)
                data[int(ls[3])][int(ls[0])-1] = 1
        data_vtk = list()
        # appending data to .vtk file
        for i in xrange(len(phys_group_list)):
            physname = phys_group_list[i]
            key = kfv(phys_group_dict, physname)
            data_vtk.append(numpy_support.numpy_to_vtk(data[key], deep=True, array_type=vtk.VTK_FLOAT))
            data_vtk[i].SetName(physname)
            meshgrid.GetCellData().AddArray(data_vtk[i])

        reader_vtk.CloseVTKFile()

        return meshgrid