import bpy

from bpy.types import Panel


class CHEMV_PT_PANEL(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Modifier operations"
    bl_category = "ChemVis Util"

    def draw(self, context):

        layout = self.layout

        row = layout.row()
        col = row.column()
        col.operator("object.vis_chem_structure", text="Visualize molecule")
        # col.operator("bpy.ops.object.modifier_add(type='ARRAY')", text="Add Array")

        # col = row.column()
        # col.operator("object.cancel_all_mods", text="Cancel all")
