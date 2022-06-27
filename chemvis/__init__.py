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
    "name" : "chemvis_util",
    "author" : "himal",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}
if "bpy" in locals():
    import importlib
    importlib.reload(CHEMVIS_OT_Apply_All_Op)
    importlib.reload(CHEMV_PT_PANEL)
else:
    from . chemvis_op import CHEMVIS_OT_Apply_All_Op
    from . chemvis_pnl import CHEMV_PT_PANEL

import bpy

classes = (CHEMVIS_OT_Apply_All_Op, CHEMV_PT_PANEL)

def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()