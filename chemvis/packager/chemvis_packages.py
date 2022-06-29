
# bl_info = {
#     "name": "Install Dependencies Example",
#     "author": "Robert Guetzkow",
#     "version": (1, 0, 2),
#     "blender": (2, 81, 0),
#     "location": "View3D > Sidebar > Example Tab",
#     "description": "Example add-on that installs a Python package",
#     "warning": "Requires installation of dependencies",
#     "wiki_url": "https://github.com/robertguetzkow/blender-python-examples/add-ons/install-dependencies",
#     "tracker_url": "https://github.com/robertguetzkow/blender-python-examples/issues",
#     "support": "COMMUNITY",
#     "category": "3D View"}

import bpy
import subprocess
from collections import namedtuple

Dependency = namedtuple("Dependency", ["module", "package", "name"])

# Declare all modules that this add-on depends on. The package and (global) name can be set to None,
# if they are equal to the module name. See import_module and ensure_and_import_module for the
# explanation of the arguments.
dependencies = (Dependency(module="matplotlib", package=None, name=None),)

dependencies_installed = False


def import_module(module_name, global_name=None):
    """
    Import a module.
    :param module_name: Module to import.
    :param global_name: (Optional) Name under which the module is imported. If None the module_name will be used.
       This allows to import under a different name with the same effect as e.g. "import numpy as np" where "np" is
       the global_name under which the module can be accessed.
    :raises: ImportError and ModuleNotFoundError
    """
    import importlib

    if global_name is None:
        global_name = module_name

    # Attempt to import the module and assign it to globals dictionary. This allow to access the module under
    # the given name, just like the regular import would.
    globals()[global_name] = importlib.import_module(module_name)


def install_pip():
    """
    Installs pip if not already present. Please note that ensurepip.bootstrap() also calls pip, which adds the
    environment variable PIP_REQ_TRACKER. After ensurepip.bootstrap() finishes execution, the directory doesn't exist
    anymore. However, when subprocess is used to call pip, in order to install a package, the environment variables
    still contain PIP_REQ_TRACKER with the now nonexistent path. This is a problem since pip checks if PIP_REQ_TRACKER
    is set and if it is, attempts to use it as temp directory. This would result in an error because the
    directory can't be found. Therefore, PIP_REQ_TRACKER needs to be removed from environment variables.
    :return:
    """

    try:
        # Check if pip is already installed
        subprocess.run([bpy.app.binary_path_python, "-m",
                       "pip", "--version"], check=True)
    except subprocess.CalledProcessError:
        import os
        import ensurepip

        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)


def install_and_import_module(module_name, package_name=None, global_name=None):
    """
    Installs the package through pip and attempts to import the installed module.
    :param module_name: Module to import.
    :param package_name: (Optional) Name of the package that needs to be installed. If None it is assumed to be equal
       to the module_name.
    :param global_name: (Optional) Name under which the module is imported. If None the module_name will be used.
       This allows to import under a different name with the same effect as e.g. "import numpy as np" where "np" is
       the global_name under which the module can be accessed.
    :raises: subprocess.CalledProcessError and ImportError
    """
    import importlib

    if package_name is None:
        package_name = module_name

    if global_name is None:
        global_name = module_name

    # Try to install the package. This may fail with subprocess.CalledProcessError
    subprocess.run([bpy.app.binary_path_python, "-m", "pip",
                   "install", package_name], check=True)

    # The installation succeeded, attempt to import the module again
    import_module(module_name, global_name)


class EXAMPLE_OT_dummy_operator(bpy.types.Operator):
    bl_idname = "chemvis.dummy_operator"
    bl_label = "Dummy Operator"
    bl_description = "This operator tries to use matplotlib."
    bl_options = {"REGISTER"}

    def execute(self, context):
        print(matplotlib.get_backend())
        return {"FINISHED"}


class EXAMPLE_PT_panel(bpy.types.Panel):
    bl_label = "Example Panel"
    bl_category = "Example Tab"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        for dependency in dependencies:
            if dependency.name is None:
                layout.label(
                    text=f"{dependency.module} {globals()[dependency.module].__version__}")
            else:
                layout.label(
                    text=f"{dependency.module} {globals()[dependency.name].__version__}")

        layout.operator(EXAMPLE_OT_dummy_operator.bl_idname)


classes = (EXAMPLE_OT_dummy_operator,
           EXAMPLE_PT_panel)


class EXAMPLE_PT_warning_panel(bpy.types.Panel):
    bl_label = "Example Warning"
    bl_category = "Example Tab"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return not dependencies_installed

    def draw(self, context):
        layout = self.layout

        lines = [f"Please install the missing dependencies for the  add-on.",
                 f"1. Open the preferences (Edit > Preferences > Add-ons).",
                 f"2. Search for the add-on.",
                 f"3. Open the details section of the add-on.",
                 f"4. Click on the \"{CHEMVIS_OT_install_dependencies.bl_label}\" button.",
                 f"   This will download and install the missing Python packages, if Blender has the required",
                 f"   permissions.",
                 f"If you're attempting to run the add-on from the text editor, you won't see the options described",
                 f"above. Please install the add-on properly through the preferences.",
                 f"1. Open the add-on preferences (Edit > Preferences > Add-ons).",
                 f"2. Press the \"Install\" button.",
                 f"3. Search for the add-on file.",
                 f"4. Confirm the selection by pressing the \"Install Add-on\" button in the file browser."]

        for line in lines:
            layout.label(text=line)


class CHEMVIS_OT_install_dependencies(bpy.types.Operator):
    bl_idname = "chemvis.install_dependencies"
    bl_label = "Install dependencies"
    bl_description = ("Downloads and installs the required python packages for this add-on. "
                      "Internet connection is required. Blender may have to be started with "
                      "elevated permissions in order to install the package")
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return not dependencies_installed

    def execute(self, context):
        try:
            install_pip()
            for dependency in dependencies:
                install_and_import_module(module_name=dependency.module,
                                          package_name=dependency.package,
                                          global_name=dependency.name)
        except (subprocess.CalledProcessError, ImportError) as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        global dependencies_installed
        dependencies_installed = True

        # Register the panels, operators, etc. since dependencies are installed
        for cls in classes:
            bpy.utils.register_class(cls)

        return {"FINISHED"}


# preference_classes = (EXAMPLE_PT_warning_panel,
#                       EXAMPLE_OT_install_dependencies,
#                       EXAMPLE_preferences)


# def register():
#     global dependencies_installed
#     dependencies_installed = False

#     for cls in preference_classes:
#         bpy.utils.register_class(cls)

#     try:
#         for dependency in dependencies:
#             import_module(module_name=dependency.module,
#                           global_name=dependency.name)
#         dependencies_installed = True
#     except ModuleNotFoundError:
#         # Don't register other panels, operators etc.
#         return

#     for cls in classes:
#         bpy.utils.register_class(cls)


# def unregister():
#     for cls in preference_classes:
#         bpy.utils.unregister_class(cls)

#     if dependencies_installed:
#         for cls in classes:
#             bpy.utils.unregister_class(cls)


# if __name__ == "__main__":
#     register()
