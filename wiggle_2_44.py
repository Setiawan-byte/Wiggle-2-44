bl_info = {
    "name": "Wiggle 2",
    "author": "Steve Miller (rewritten for Blender 4.4 by ChatGPT)",
    "version": (2, 3, 0),
    "blender": (4, 4, 0),
    "location": "3D Viewport > Sidebar > Animation Tab",
    "description": "Simulate spring-like physics on Bone transforms with improved compatibility and structure",
    "category": "Animation",
}

import bpy
from mathutils import Vector, Matrix
from bpy.app.handlers import persistent
import mathutils.bvhtree

# (Previous content remains unchanged: PropertyGroups, simulate_bone, wiggle_frame_update)

# ------------------------------------------------------------------------
#    Utilities: Copy / Reset Bone States
# ------------------------------------------------------------------------

def reset_wiggle_bone(bone):
    if not hasattr(bone, "wiggle"):
        return
    bone.wiggle.position = bone.tail
    bone.wiggle.position_last = bone.tail
    bone.wiggle.velocity = (0.0, 0.0, 0.0)
    bone.wiggle.position_head = bone.head
    bone.wiggle.position_last_head = bone.head
    bone.wiggle.velocity_head = (0.0, 0.0, 0.0)

def copy_wiggle_settings(source_bone, target_bone):
    if not hasattr(source_bone, "wiggle") or not hasattr(target_bone, "wiggle"):
        return
    target_bone.wiggle.collision_ob = source_bone.wiggle.collision_ob

# ------------------------------------------------------------------------
#    UI Panel in Sidebar
# ------------------------------------------------------------------------

class WigglePanel(bpy.types.Panel):
    bl_label = "Wiggle Physics"
    bl_idname = "VIEW3D_PT_wiggle_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Animation'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if not hasattr(scene, 'wiggle'):
            layout.label(text="Wiggle not initialized.")
            return

        layout.prop(scene.wiggle, "iterations")
        layout.prop(scene.wiggle, "loop")
        layout.prop(scene.wiggle, "preroll")
        layout.prop(scene.wiggle, "bake_overwrite")
        layout.prop(scene.wiggle, "bake_nla")
        layout.prop(scene.wiggle, "reset")

        layout.separator()
        layout.label(text="Per-Bone Settings")
        bone = context.active_pose_bone
        if bone:
            layout.prop(bone.wiggle, "collision_ob", text="Collision Object")
            layout.operator("wiggle.reset_bone", icon='RECOVER_AUTO')
            layout.operator("wiggle.copy_settings", icon='COPYDOWN')
        else:
            layout.label(text="Select a pose bone")

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class WIGGLE_OT_ResetBone(bpy.types.Operator):
    bl_idname = "wiggle.reset_bone"
    bl_label = "Reset Wiggle Bone"

    def execute(self, context):
        bone = context.active_pose_bone
        if bone:
            reset_wiggle_bone(bone)
            self.report({'INFO'}, f"Wiggle state reset for {bone.name}")
        return {'FINISHED'}

class WIGGLE_OT_CopySettings(bpy.types.Operator):
    bl_idname = "wiggle.copy_settings"
    bl_label = "Copy Wiggle to Selected"

    def execute(self, context):
        active = context.active_pose_bone
        selected = context.selected_pose_bones
        for bone in selected:
            if bone != active:
                copy_wiggle_settings(active, bone)
        self.report({'INFO'}, "Copied wiggle settings to selected bones.")
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    WiggleBoneItem,
    WiggleItem,
    WiggleScene,
    WiggleBoneState,
    WigglePanel,
    WIGGLE_OT_ResetBone,
    WIGGLE_OT_CopySettings,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.wiggle = bpy.props.PointerProperty(type=WiggleScene)
    bpy.types.PoseBone.wiggle = bpy.props.PointerProperty(type=WiggleBoneState)
    bpy.app.handlers.frame_change_post.append(wiggle_frame_update)

def unregister():
    bpy.app.handlers.frame_change_post.remove(wiggle_frame_update)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.wiggle
    del bpy.types.PoseBone.wiggle

if __name__ == "__main__":
    register()
