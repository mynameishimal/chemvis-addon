import bpy
from bpy.types import Operator

class CHEMVIS_OT_Apply_All_Op(Operator):
    bl_idname="object.apply_all_mods"
    bl_label="Apply all"
    bl_description="Apply all operators of the active object"


    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode=="OBJECT":
                return True

        return False

    def execute(self, context):
        active_obj = context.view_layer.objects.active

        for mod in active_obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=mod.name)

        return {"FINISHED"}

class CHEMVIS_OT_Cancel_All_Op(Operator):
    bl_idname="object.cancel_all_mods"
    bl_label="Cancel all"
    bl_description="Cancel all operators of the active object"

    
    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode=="OBJECT":
                return True

        return False

    def execute(self, context):
        active_obj = context.view_layer.objects.active

        for mod in active_obj.modifiers:
            bpy.ops.object.modifier_remove(modifier=mod.name)

        return {"FINISHED"}

class ObjectVisualizeX(Operator):
    bl_idname="object.plot_atoms"
    bl_label="Plot atoms"
    bl_description="Plot atoms in coordinate space"

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode=="OBJECT":
                return True

        return False

    # def execute(self, context):
    #         atomCoordinates = getCoordinates(ind)
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

    #     return {"FINISHED"}