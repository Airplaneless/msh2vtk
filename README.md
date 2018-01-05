# msh2vtk
Convert GMSH file .msh to vtkUnstructedGrid .vtk with saving physical groups

That's simple

        GMSH_PATH = 'gmsh'
        
        converter = MSH2VTK(GMSH_PATH, 'cubic.msh')
        ugrid = converter.convert()