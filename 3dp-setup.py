bl_info = {
    "name": "Setup project for 3D printing",
    "author": "rayps",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "location": "File -> New (Ctrl + N)",
    "description": "Setup project for 3D printing",
    "warning": "",
    "doc_url": "https://github.com/rayps/blender-3dp-setup",
    "tracker_url": "https://github.com/rayps/blender-3dp-setup/issues",
    "category": "Scene",
}

import bpy

class SetupProjectFor3DPrinting(bpy.types.Operator):
    bl_idname = "object.setup_project_for_3d_printing"
    bl_label = "Setup project for 3D printing"
    bl_options = {"REGISTER", "UNDO"}

    prop_delete_all: bpy.props.BoolProperty(name = "Delete Everything", default=False)
    prop_build_plate: bpy.props.BoolProperty(name = "Create Build Plate", default=False)
    prop_build_plate_size: bpy.props.IntProperty(name = "Size", default=220, min=0)
    prop_build_plate_shape: bpy.props.EnumProperty(name = "Build Plate Shape", items={("SQUARE", "Square", ""), ("CIRCLE", "Circle", "")})


    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        # Unit
        scene = context.scene
        scene.unit_settings.scale_length = 0.001
        scene.unit_settings.system = 'METRIC'
        scene.unit_settings.length_unit = 'MILLIMETERS'

        # Viewport
        workspaces = bpy.data.workspaces
        for workspace in workspaces:
            for screen in workspace.screens:
                for area in screen.areas:
                    if area.type == 'VIEW_3D':
                        for space in area.spaces: 
                            if space.type == 'VIEW_3D':
                                space.clip_start = 0.1
                                space.overlay.grid_scale = 0.001
                                space.overlay.show_extra_edge_length = True
                                space.overlay.show_statvis = True
                                space.shading.light = 'MATCAP'
                                space.shading.show_cavity = True
                                space.shading.cavity_type = 'BOTH'

                    if area.type == 'OUTLINER':
                        for space in area.spaces: 
                            if space.display_mode == 'VIEW_LAYER':
                                space.show_restrict_column_select = True
        
        # Exit edit mode
        if (context.mode == 'EDIT_MESH'):
            bpy.ops.object.editmode_toggle()

        # Delete everything
        if (self.prop_delete_all):
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()

        # Create build plate
        if (self.prop_build_plate and self.prop_build_plate_size > 0):
            if (self.prop_build_plate_shape == "SQUARE"):
                bpy.ops.mesh.primitive_plane_add(size=self.prop_build_plate_size, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            else:
                bpy.ops.mesh.primitive_circle_add(radius=self.prop_build_plate_size / 2, fill_type='NGON', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            bpy.context.object.name = "Build Plate"

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        layout.label(text="Optional Operations:")

        box = layout.box()
        box.prop(self, "prop_delete_all")

        row = box.row()

        col = row.column()
        col.prop(self, "prop_build_plate")
        col.ui_units_x = 0.5

        col = row.column()
        col.prop(self, "prop_build_plate_size")
        col.ui_units_x = 0.4
        col.enabled = self.prop_build_plate

        col = row.column()
        col.label(text="mm")
        col.ui_units_x = 0.1

        row = box.row()
        row.alignment = "RIGHT"
        row.label(text="Shape")
        row.prop(self, "prop_build_plate_shape", text="")
        row.enabled = self.prop_build_plate


def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(SetupProjectFor3DPrinting.bl_idname)


def register():
    bpy.utils.register_class(SetupProjectFor3DPrinting)
    bpy.types.TOPBAR_MT_file_new.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SetupProjectFor3DPrinting)
    bpy.types.TOPBAR_MT_file_new.remove(menu_func)


if __name__ == "__main__":
    register()

