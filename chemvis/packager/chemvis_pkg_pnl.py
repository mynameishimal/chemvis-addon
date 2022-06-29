import bpy
class CHEMVIS_dep_install_panel(bpy.types.AddonPreferences):
    bl_idname = "chemvis"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "chemvis.install_dependencies", icon="CONSOLE")
