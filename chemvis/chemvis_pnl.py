import bpy

from bpy.types import Panel

class CHEMV_PT_PANEL(Panel):
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_label="Modifier operations"
    bl_category="ChemVis Util"

    def draw (self, context):

        layout = self.layout

        row = layout.row()
        col = row.column()
        col.operator("object.apply_all_mods", text="Apply all")

        col = row.column()
        col.operator("object.cancel_all_mods", text="Cancel all")
