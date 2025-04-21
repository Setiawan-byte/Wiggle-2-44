Wiggle 2 Blender 4 4
Anda sedang melihat konten buatan pengguna yang mungkin belum diverifikasi atau tidak aman.
Laporkan

Jalankan
ChatGPT
Edit dengan ChatGPT

54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
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

