# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


bl_info = {
    "name": "chemvis",
    "author": "himal",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "View3D",
    "warning": "",
    "category": "Object"
}

if "bpy" in locals():
    import importlib
    importlib.reload(A)
    importlib.reload(CHEMV_PT_PANEL)
    importlib.reload(CHEMVIS_OT_install_dependencies)
    importlib.reload(CHEMVIS_dep_install_panel)
    importlib.reload(import_module)

else:
    from .chemvis_op import CHEMVIS_OT_Apply_All_Op
    from .chemvis_pnl import CHEMV_PT_PANEL
    from .packager.chemvis_packages import CHEMVIS_OT_install_dependencies
    from .packager.chemvis_packages import import_module
    from .packager.chemvis_pkg_pnl import CHEMVIS_dep_install_panel
# bpy.ops.mesh.primitive_ico_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0.437286, 1.08707, -0.192946), scale=(1, 1, 1))

import bpy
import subprocess
from collections import namedtuple

Dependency = namedtuple("Dependency", ["module", "package", "name"])

# Declare all modules that this add-on depends on. The package and (global) name can be set to None,
# if they are equal to the module name. See import_module and ensure_and_import_module for the
# explanation of the arguments.
dependencies = (Dependency(module="scipy", package=None, name=None),)

dependencies_installed = False
# classes = (CHEMVIS_OT_Apply_All_Op, CHEMV_PT_PANEL,
#            )


class EXAMPLE_preferences(bpy.types.AddonPreferences):
    bl_idname = "chemvis"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            CHEMVIS_OT_install_dependencies.bl_idname, icon="CONSOLE")


preference_classes = (CHEMVIS_OT_install_dependencies,
                      CHEMVIS_dep_install_panel)

classes = (CHEMVIS_OT_Apply_All_Op, CHEMV_PT_PANEL,)


def register():
    global dependencies_installed
    dependencies_installed = False

    for cls in preference_classes:
        bpy.utils.register_class(cls)

    try:
        for dependency in dependencies:
            import_module(module_name=dependency.module,
                          global_name=dependency.name)
        dependencies_installed = True
    except ModuleNotFoundError:
        # Don't register other panels, operators etc.
        return
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for cls in preference_classes:
        bpy.utils.unregister_class(cls)

    if dependencies_installed:
        for cls in classes:
            bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
