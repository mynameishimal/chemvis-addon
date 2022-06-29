import scipy.io as sio
import numpy as np
import bpy
mat_fname = "qm7.mat"
mat_contents = sio.loadmat(mat_fname)
print(mat_contents)
atomCoord = mat_contents.get("R")

chem1_atomCoord = atomCoord[0]

print(chem1_atomCoord.shape)


def mapAtoms(ind=0):
    atomCoordinates = getCoordinates(ind)
    for x in atomCoordinates:
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.location[0] = x[0]
        bpy.context.object.location[1] = x[1]
        bpy.context.object.location[2] = x[2]
        bpy.context.object.scale[0] = 0.2
        bpy.context.object.scale[1] = 0.2
        bpy.context.object.scale[2] = 0.2


def getCoordinates(ind=0):
    return atomCoord[ind]
