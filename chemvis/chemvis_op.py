from operator import index
import bpy
from bpy.types import Operator
import scipy.io as sio

from . import utils


class CHEMVIS_OT_Vis_Chem_Structure(Operator):
    bl_idname = "object.vis_chem_structure"
    bl_label = "Show chemical"
    bl_description = "shows 3d representation of small molecule"

    def execute(self, context):
        # ensure_collection = utils.ensure_collection()
        mat_fname = "qm7.mat"
        mat_contents = sio.loadmat(mat_fname)
        atomCoord = mat_contents.get("R")
        ind = 0
        atomCoordinates = atomCoord[ind]

        for index, coord in enumerate(atomCoordinates):
            # print(x)
            if coord[0] != 0 and coord[1] != 0 and coord[2] != 0:
                bpy.ops.mesh.primitive_ico_sphere_add(
                    radius=0.2, enter_editmode=False, align='WORLD', location=(coord[0], coord[1], coord[2]), scale=(1, 1, 1))
                sphere = context.active_object
                sphere.name = "atom" + str(index)
        return {"FINISHED"}

    # def execute(self, context):
    #     active_obj = context.view_layer.objects.active

    #     for mod in active_obj.modifiers:
    #         bpy.ops.object.modifier_apply(modifier=mod.name)

    #     return {"FINISHED"}

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode == "OBJECT":
                return True

        return False

    # def execute(self, context):
    #     active_obj = context.view_layer.objects.active

    #     for mod in active_obj.modifiers:
    #         bpy.ops.object.modifier_apply(modifier=mod.name)

    #     return {"FINISHED"}


# class CHEMVIS_OT_Cancel_All_Op(Operator):
#     bl_idname = "object.cancel_all_mods"
#     bl_label = "Cancel all"
#     bl_description = "Cancel all operators of the active object"

#     @classmethod
#     def poll(cls, context):
#         obj = context.object

#         if obj is not None:
#             if obj.mode == "OBJECT":
#                 return True

#         return False

#     def execute(self, context):
#         active_obj = context.view_layer.objects.active

#         for mod in active_obj.modifiers:
#             bpy.ops.object.modifier_remove(modifier=mod.name)

#         return {"FINISHED"}

# class ObjectVisualizeX(Operator):
#     bl_idname="object.plot_atoms"
#     bl_label="Plot atoms"
#     bl_description="Plot atoms in coordinate space"

#     @classmethod
#     def poll(cls, context):
#         obj = context.object

#         if obj is not None:
#             if obj.mode=="OBJECT":
#                 return True

#         return False

#     def execute(self, context):
#         mat_fname = "qm7.mat"
#         mat_contents=sio.loadmat(mat_fname)
#         atomCoord = mat_contents.get("R")
#         ind = 0
#         atomCoordinates = atomCoord[ind]
#         for x in atomCoordinates:
#             bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
#             bpy.context.object.location[0] = x[0]
#             bpy.context.object.location[1] = x[1]
#             bpy.context.object.location[2] = x[2]
#             bpy.context.object.scale[0] = 0.2
#             bpy.context.object.scale[1] = 0.2
#             bpy.context.object.scale[2] = 0.2
#         for mod in active_obj.modifiers:
#             bpy.ops.object.modifier_apply(modifier=mod.name)

#         return {"FINISHED"}


class ObjectMoveX(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.move_x"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Move X by One"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # execute() is called when running the operator.
    def execute(self, context):

        # The original script
        scene = context.scene
        for obj in scene.objects:
            obj.location.x += 1.0

        # Lets Blender know the operator finished successfully.
        return {'FINISHED'}
