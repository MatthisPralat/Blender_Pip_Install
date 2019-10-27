# by matthis pralat, matthispralat.fr
# with the help of Legigan Jeremy aka Pistiwique
# And s-Leger from Archipack
# thanks to blender lounge community

'''

Init Interface for Material Utils 

'''

import bpy
import subprocess
import os
import sys


def verify_python_version(self):
    PYPATH = bpy.app.binary_path_python
    print(PYPATH)

    # GET BLENDER PYTHON VERSION ----
    BPV = sys.version_info
    BlenderPythonVersionBase = r"Python " + str(BPV[0]) + "." + str(BPV[1]) + "." + str(BPV[2]) + "  "
    BlenderPythonVersion = BlenderPythonVersionBase.strip()
    # BlenderPythonVersion = BlenderPythonVersion.replace(" ", "")
    print(BlenderPythonVersion.strip())

    # GET WINDOWS PYTHON VERSION INSTALLED ---
    result = subprocess.run(['python', '-V'], stdout=subprocess.PIPE)
    WindowsPythonVersion = str(result.stdout.decode('utf-8'))
    WindowsPythonVersion = WindowsPythonVersion.strip()

    if BlenderPythonVersion == WindowsPythonVersion:
        m1 = "your python path in your command is the same as blender"
        m2 = "All is good "
        msg = m1
        return (True, msg)

    else:
        m1 = "your python path in your command is not the same as blender"
        m2 = "Please install the same version and set as path"
        m3 = "Install" + BlenderPythonVersionBase
        msg = m1 + m2  + m3
        return( False , msg )


def module_installed(self):
    ''' '''
    print('mom module: ', self)
    moduleStatus = True
    try:
        code = 'import ' + self
        exec (code)
    except ImportError:
        moduleStatus = False

    if moduleStatus == False:
        print('module', self, 'not set')
    if moduleStatus == True:
        print('module', self, 'is set')
    return moduleStatus

# Main ui
class MaterialUtilsPanel2(bpy.types.Panel):
    bl_label = "Pip Module"
    bl_idname = "PIP_UTILS_PANEL_PT_VIEW3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "pip"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Pip Install")
        props = context.scene.PipUtilsPropertyGroup

        row = layout.row()
        PyStatut, PyMsg= verify_python_version(self)

        if PyStatut == False:
            layout.label( text=PyMsg)
            row = layout.row()
            BPV = sys.version_info
            PV = r"Python " + str(BPV[0]) + "." + str(BPV[1]) + "." + str(BPV[2]) + "  "
            row.operator('wm.url_open', text='Install Python').url = 'https://www.python.org/downloads/release/python-'+ str(BPV[0]) + str(BPV[1]) + str(BPV[2]) + '/'

        if PyStatut == True:
            layout.label(text=PyMsg)

        if module_installed('pip') == False :
            layout.label(text="Install pip ")
            row = layout.row()
            row.operator("modules_utils.pip_install")

        if module_installed('pip') == True :
            layout.label(text="pip is installed")

        # Custom Module ----------------
        layout.label(text="Custom pip Module ")
        box = layout.box()
        row = box.row()
        row.prop(props, "newModuleName")
        row = box.row()
        row.operator("modules_utils.pip_custom")
        row.operator("modules_utils.unpip_custom")

        layout.label(text=" Open Console to follow installation")
        row = layout.row()
        row.operator('wm.console_toggle')




class PipUtilsPropertyGroup( bpy.types.PropertyGroup ):
    # Init Linked Library Update
    newModuleName: bpy.props.StringProperty(name="",  default = "PySide2")

# -- Operator ------

class Pip:

    def __init__(self, module=None, action="install", options=None):
        if module is not None:
            self.ensurepip()
            self._cmd(action, options, module)

    def _cmd(self, action, options, module):
        PYPATH = bpy.app.binary_path_python
        cmd = [PYPATH, "-m", "pip", action]
        if options is not None:
            cmd.extend(options)
        cmd.append(module)
        self.run(cmd)

    def _run(self, cmd):
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
        popen.stdout.close()
        popen.wait()

    def run(self, cmd):
        for res in self._run(cmd):
            if "ERROR:" in res:
                raise Exception(res)
            print(res)

    def ensurepip(self):
        pip_not_found = False
        try:
            import pip
        except ImportError:
            pip_not_found = True
            pass
        if pip_not_found:
            print("install pip")
            PYPATH = bpy.app.binary_path_python
            self.run([PYPATH, "-m", "ensurepip"])
            self._cmd("install", ["--upgrade"], "pip")
        else:
            print("pip already install")

    @staticmethod
    def uninstall(module, options=None):
        if options is None:
            # force confirm
            options = ["-y"]
        Pip(module, "uninstall", options)

    @staticmethod
    def install(module, options=None):
        Pip(module, "install", options)



class install_pip(bpy.types.Operator):
    '''Instal pip'''
    bl_idname = "modules_utils.pip_install"
    bl_label = "Install pip"

    def execute(self, context):
        Pip(self)
        return {"FINISHED"}

class install_pyside2(bpy.types.Operator):
    '''Instaling PySide2 from PIP into your blender. Can be long, watch your system Console.'''
    bl_idname = "modules_utils.pip_pyside2"
    bl_label = "Install PySide2"
    def execute(self, context):
        print("hello")
        Pip.install("PySide2", options=["--user"])
        return {"FINISHED"}

class uninstall_pyside2(bpy.types.Operator):
    '''Uninstall Pyside 2'''
    bl_idname = "modules_utils.unpip_pyside2"
    bl_label = "Uninstall PySide2"
    def execute(self, context):
        print("hello")
        Pip.uninstall("PySide2")
        return {"FINISHED"}

class install_module(bpy.types.Operator):
    '''Instaling PySide2 from PIP into your blender. Can be long, watch your system Console.'''
    bl_idname = "modules_utils.pip_custom"
    bl_label = "Install Module"

    def execute(self, context):
        props = context.scene.PipUtilsPropertyGroup
        module =  props.newModuleName
        Pip.install( module, options=["--user"])
        return {"FINISHED"}


class uninstall_module(bpy.types.Operator):
    '''Instaling PySide2 from PIP into your blender. Can be long, watch your system Console.'''
    bl_idname = "modules_utils.unpip_custom"
    bl_label = "Uninstall Module"
    def execute(self, context):
        props = context.scene.PipUtilsPropertyGroup
        module = props.newModuleName
        Pip.uninstall(module)
        return {"FINISHED"}

# -- Functions ------
# check module validity
def module_installed(self):
    print('mom module: ', self)
    moduleStatus = True
    try:
        code = 'import ' + self
        exec (code)
    except ImportError:
        moduleStatus = False

    if moduleStatus == False:
        print('module', self, 'not set')
    if moduleStatus == True:
        print('module', self, 'is set')

    return moduleStatus

# -----------------------------
# REGISTER / UNREGISTER / INIT
#------------------------------

classes = [
    install_pip,
    install_module,
    uninstall_module,
    PipUtilsPropertyGroup,
    install_pyside2,
    uninstall_pyside2,
    MaterialUtilsPanel2,
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.PipUtilsPropertyGroup = bpy.props.PointerProperty(type=PipUtilsPropertyGroup)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()