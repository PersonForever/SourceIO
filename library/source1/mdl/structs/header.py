from enum import IntFlag

from . import Base, ByteIO


class StudioHDRFlags(IntFlag):
    AUTOGENERATED_HITBOX = (1 << 0)
    #  NOTE:  This flag is set at loadtime, not mdl build time so that we don't have to rebuild
    #  models when we change materials.
    USES_ENV_CUBEMAP = (1 << 1)
    # Use this when there are translucent parts to the model but we're not
    # going to sort it
    FORCE_OPAQUE = (1 << 2)
    #  Use this when we want to render the opaque parts during the opaque pass
    #  and the translucent parts during the translucent pass
    TRANSLUCENT_TWOPASS = (1 << 3)
    #  This is set any time the .qc files has $staticprop in it
    #  Means there's no bones and no transforms
    STATIC_PROP = (1 << 4)
    #  NOTE:  This flag is set at loadtime, not mdl build time so that we don't have to rebuild
    #  models when we change materials.
    USES_FB_TEXTURE = (1 << 5)
    #  This flag is set by studiomdl.exe if a separate "$shadowlod" entry was present
    #   for the .mdl (the shadow lod is the last entry in the lod list if present)
    HASSHADOWLOD = (1 << 6)
    #  NOTE:  This flag is set at loadtime, not mdl build time so that we don't have to rebuild
    #  models when we change materials.
    USES_BUMPMAPPING = (1 << 7)
    #  NOTE:  This flag is set when we should use the actual materials on the shadow LOD
    # instead of overriding them with the default one (necessary for
    # translucent shadows)
    USE_SHADOWLOD_MATERIALS = (1 << 8)
    #  NOTE:  This flag is set when we should use the actual materials on the shadow LOD
    # instead of overriding them with the default one (necessary for
    # translucent shadows)
    OBSOLETE = (1 << 9)
    UNUSED = (1 << 10)
    #  NOTE:  This flag is set at mdl build time
    NO_FORCED_FADE = (1 << 11)
    # NOTE:  The npc will lengthen the viseme check to always include two
    # phonemes
    FORCE_PHONEME_CROSSFADE = (1 << 12)
    #  This flag is set when the .qc has $constantdirectionallight in it
    #  If set, we use constantdirectionallightdot to calculate light intensity
    #  rather than the normal directional dot product
    #  only valid if STATIC_PROP is also set
    CONSTANT_DIRECTIONAL_LIGHT_DOT = (1 << 13)
    # Flag to mark delta flexes as already converted from disk format to
    # memory format
    FLEXES_CONVERTED = (1 << 14)
    #  Indicates the studiomdl was built in preview mode
    BUILT_IN_PREVIEW_MODE = (1 << 15)
    #  Ambient boost (runtime flag)
    AMBIENT_BOOST = (1 << 16)
    #  Don't cast shadows from this model (useful on first-person models)
    DO_NOT_CAST_SHADOWS = (1 << 17)
    # alpha textures should cast shadows in vrad on this model (ONLY prop_static!)
    CAST_TEXTURE_SHADOWS = (1 << 18)
    SUBDIVISION_SURFACE = (1 << 19)
    #  flagged on load to indicate no animation events on this model
    VERT_ANIM_FIXED_POINT_SCALE = (1 << 21)


class MdlHeaderV36(Base):
    def __init__(self):
        self.id = ''
        self.version = 0
        self.checksum = 0
        self.name = ''
        self.second_name = ''
        self.file_size = 0
        self.eye_position = []
        self.illumination_position = []
        self.hull_min = []
        self.hull_max = []
        self.view_bbox_min = []
        self.view_bbox_max = []

        self.flags = StudioHDRFlags(0)
        self.bone_count = 0
        self.bone_offset = 0
        self.bone_controller_count = 0
        self.bone_controller_offset = 0
        self.hitbox_set_count = 0
        self.hitbox_set_offset = 0
        self.local_animation_count = 0
        self.local_animation_offset = 0
        self.local_sequence_count = 0
        self.local_sequence_offset = 0
        self.sequences_indexed_flag = 0
        self.sequence_group_count = 0
        self.sequence_group_offset = 0
        self.activity_list_version = 0
        self.events_indexed = 0
        self.texture_count = 0
        self.texture_offset = 0
        self.texture_path_count = 0
        self.texture_path_offset = 0
        self.skin_reference_count = 0
        self.skin_family_count = 0
        self.skin_family_offset = 0
        self.body_part_count = 0
        self.body_part_offset = 0
        self.local_attachment_count = 0
        self.local_attachment_offset = 0
        self.transition_count = 0
        self.transition_offset = 0
        self.sound_table = 0
        self.sound_index = 0
        self.sound_groups = 0
        self.sound_group_offset = 0
        self.local_node_count = 0
        self.local_node_offset = 0
        self.local_node_name_offset = 0
        self.flex_desc_count = 0
        self.flex_desc_offset = 0
        self.flex_controller_count = 0
        self.flex_controller_offset = 0
        self.flex_rule_count = 0
        self.flex_rule_offset = 0
        self.ik_chain_count = 0
        self.ik_chain_offset = 0
        self.mouth_count = 0
        self.mouth_offset = 0
        self.local_pose_paramater_count = 0
        self.local_pose_parameter_offset = 0
        self.surface_prop = ''
        self.key_value_offset = 0
        self.key_value_size = 0
        self.local_ik_auto_play_lock_count = 0
        self.local_ik_auto_play_lock_offset = 0
        self.mass = 0.0
        self.contents = 0
        self.reserved = []

        self.anim_block_relative_path_file_name = ""

        self.name_offset = 0

        self.max_eye_deflection = 0

    @classmethod
    def is_valid_file(cls, reader: ByteIO):
        with reader.save_current_pos():
            fourcc = reader.read_fourcc()
        return fourcc == "IDST"

    def read(self, reader: ByteIO):
        self.id = reader.read_fourcc()
        self.version, self.checksum = reader.read_fmt('ii')
        self.store_value('mdl_version', self.version)
        self.name = reader.read_ascii_string(64)
        self.file_size = reader.read_uint32()

        self.eye_position = reader.read_fmt('3f')
        self.illumination_position = reader.read_fmt('3f')
        self.hull_min = reader.read_fmt('3f')
        self.hull_max = reader.read_fmt('3f')

        self.view_bbox_min = reader.read_fmt('3f')
        self.view_bbox_max = reader.read_fmt('3f')

        self.flags = StudioHDRFlags(reader.read_uint32())

        self.bone_count, self.bone_offset = reader.read_fmt('2I')
        self.bone_controller_count, self.bone_controller_offset = reader.read_fmt('2I')

        self.hitbox_set_count, self.hitbox_set_offset = reader.read_fmt('2I')

        self.local_animation_count, self.local_animation_offset = reader.read_fmt('2I')
        self.local_sequence_count, self.local_sequence_offset = reader.read_fmt('2I')
        reader.skip(16)
        self.sequences_indexed_flag, self.sequence_group_count = reader.read_fmt('2I')
        self.sequence_group_offset = reader.read_int32()

        self.texture_count, self.texture_offset = reader.read_fmt('2I')
        self.texture_path_count, self.texture_path_offset = reader.read_fmt('2I')
        self.skin_reference_count, self.skin_family_count, self.skin_family_offset = reader.read_fmt('3I')

        self.body_part_count, self.body_part_offset = reader.read_fmt('2I')
        self.local_attachment_count, self.local_attachment_offset = reader.read_fmt('2I')

        self.transition_count, self.transition_offset = reader.read_fmt('2I')

        self.flex_desc_count, self.flex_desc_offset = reader.read_fmt('2I')
        self.flex_controller_count, self.flex_controller_offset = reader.read_fmt('2I')
        self.flex_rule_count, self.flex_rule_offset = reader.read_fmt('2I')

        self.ik_chain_count, self.ik_chain_offset = reader.read_fmt('2I')
        self.mouth_count, self.mouth_offset = reader.read_fmt('2I')
        self.local_pose_paramater_count, self.local_pose_parameter_offset = reader.read_fmt('2I')

        self.surface_prop = reader.read_source1_string(0)

        self.key_value_offset, self.key_value_size = reader.read_fmt('2I')
        self.local_ik_auto_play_lock_count, self.local_ik_auto_play_lock_offset = reader.read_fmt('2I')
        self.mass, self.contents = reader.read_fmt('fI')

        self.reserved = reader.read_fmt('9i')


class MdlHeaderV44(MdlHeaderV36):
    def __init__(self):
        super().__init__()
        self.include_model_count = 0
        self.include_model_offset = 0
        self.virtual_model_pointer = 0
        self.anim_block_name = ""
        self.anim_block_count = 0
        self.anim_block_offset = 0
        self.anim_block_model_pointer = 0
        self.bone_table_by_name_offset = 0
        self.vertex_base_pointer = 0
        self.index_base_pointer = 0
        self.directional_light_dot = 0
        self.root_lod = 0
        self.unused = 0
        self.zero_frame_cache_offset = 0
        self.unused4 = []
        self.flex_controller_ui_count = 0
        self.flex_controller_ui_offset = 0
        self.vert_anim_fixed_point_scale = 0
        self.surface_prop_lookup = 0
        self.unused3 = []
        self.studio_header2_offset = 0
        self.bone_flex_driver_count = 0
        self.bone_flex_driver_offset = 0
        self.unused2 = 0

        self.source_bone_transform_count = 0
        self.source_bone_transform_offset = 0
        self.illum_position_attachment_index = 0
        self.max_eye_deflection = 0
        self.linear_bone_offset = 0
        self.name2_offset = 0
        self.actual_file_size = 0

    def read(self, reader: ByteIO):
        self.id = reader.read_fourcc()
        self.version, self.checksum = reader.read_fmt('ii')
        self.store_value('mdl_version', self.version)
        self.name = reader.read_ascii_string(64)
        self.file_size = reader.read_uint32()

        self.eye_position = reader.read_fmt('3f')
        self.illumination_position = reader.read_fmt('3f')
        self.hull_min = reader.read_fmt('3f')
        self.hull_max = reader.read_fmt('3f')

        self.view_bbox_min = reader.read_fmt('3f')
        self.view_bbox_max = reader.read_fmt('3f')

        self.flags = StudioHDRFlags(reader.read_uint32())

        self.bone_count, self.bone_offset = reader.read_fmt('2I')
        self.bone_controller_count, self.bone_controller_offset = reader.read_fmt('2I')

        self.hitbox_set_count, self.hitbox_set_offset = reader.read_fmt('2I')

        self.local_animation_count, self.local_animation_offset = reader.read_fmt('2I')
        self.local_sequence_count, self.local_sequence_offset = reader.read_fmt('2I')
        self.activity_list_version, self.events_indexed = reader.read_fmt('2I')

        self.texture_count, self.texture_offset = reader.read_fmt('2I')
        self.texture_path_count, self.texture_path_offset = reader.read_fmt('2I')
        self.skin_reference_count, self.skin_family_count, self.skin_family_offset = reader.read_fmt('3I')

        self.body_part_count, self.body_part_offset = reader.read_fmt('2I')
        self.local_attachment_count, self.local_attachment_offset = reader.read_fmt('2I')
        self.local_node_count, self.local_node_offset, self.local_node_name_offset = reader.read_fmt('3I')

        self.flex_desc_count, self.flex_desc_offset = reader.read_fmt('2I')
        self.flex_controller_count, self.flex_controller_offset = reader.read_fmt('2I')
        self.flex_rule_count, self.flex_rule_offset = reader.read_fmt('2I')

        self.ik_chain_count, self.ik_chain_offset = reader.read_fmt('2I')
        self.mouth_count, self.mouth_offset = reader.read_fmt('2I')

        self.local_pose_paramater_count, self.local_pose_parameter_offset = reader.read_fmt('2I')

        self.surface_prop = reader.read_source1_string(0)

        self.key_value_offset, self.key_value_size = reader.read_fmt('2I')
        self.local_ik_auto_play_lock_count, self.local_ik_auto_play_lock_offset = reader.read_fmt('2I')
        self.mass, self.contents = reader.read_fmt('fI')

        self.include_model_count, self.include_model_offset = reader.read_fmt('2I')
        self.virtual_model_pointer = reader.read_uint32()
        self.anim_block_name = reader.read_source1_string(0)
        self.anim_block_count, self.anim_block_offset = reader.read_fmt('2I')

        self.anim_block_model_pointer, self.bone_table_by_name_offset = reader.read_fmt('2I')

        self.vertex_base_pointer, self.index_base_pointer = reader.read_fmt('2I')

        self.directional_light_dot, self.root_lod, *self.unused = reader.read_fmt('4b')
        self.zero_frame_cache_offset = reader.read_int32()

        _, scal = reader.peek_fmt('2I')
        if scal == 1279345491:
            reader.skip(5 * 4)
        self.flex_controller_ui_count, self.flex_controller_ui_offset = reader.read_fmt('2I')
        self.unused3 = reader.read_fmt('4I')

        self.studio_header2_offset, self.unused2 = reader.read_fmt('2I')
        reader.skip(4 * 9)
        self.source_bone_transform_count, self.source_bone_transform_offset = reader.read_fmt('2I')
        self.illum_position_attachment_index, self.max_eye_deflection = reader.read_fmt('If')
        self.linear_bone_offset, self.name_offset = reader.read_fmt('2I')

        self.reserved = reader.read_fmt('58i')


class MdlHeaderV49(MdlHeaderV44):
    def __init__(self):
        super().__init__()
        self.allowed_root_lod_count = 0
        self.source_bone_transform_count = 0
        self.source_bone_transform_offset = 0
        self.bone_flex_driver_offset = 0
        self.illum_position_attachment_index = 0
        self.max_eye_deflection = 0
        self.linear_bone_offset = 0
        self.section_frame_count = 0
        self.section_frame_min_frame_count = 0
        self.actual_file_size = 0

    def read(self, reader: ByteIO):
        self.id = reader.read_fourcc()
        self.version, self.checksum = reader.read_fmt('ii')
        self.store_value('mdl_version', self.version)
        self.name = reader.read_ascii_string(64)
        self.file_size = reader.read_uint32()
        assert self.file_size == reader.size()

        self.eye_position = reader.read_fmt('3f')
        self.illumination_position = reader.read_fmt('3f')
        self.hull_min = reader.read_fmt('3f')
        self.hull_max = reader.read_fmt('3f')

        self.view_bbox_min = reader.read_fmt('3f')
        self.view_bbox_max = reader.read_fmt('3f')

        self.flags = StudioHDRFlags(reader.read_uint32())

        self.bone_count, self.bone_offset = reader.read_fmt('2I')
        self.bone_controller_count, self.bone_controller_offset = reader.read_fmt('2I')

        self.hitbox_set_count, self.hitbox_set_offset = reader.read_fmt('2I')

        self.local_animation_count, self.local_animation_offset = reader.read_fmt('2I')
        self.local_sequence_count, self.local_sequence_offset = reader.read_fmt('2I')
        self.activity_list_version, self.events_indexed = reader.read_fmt('2I')

        self.texture_count, self.texture_offset = reader.read_fmt('2I')
        self.texture_path_count, self.texture_path_offset = reader.read_fmt('2I')
        self.skin_reference_count, self.skin_family_count, self.skin_family_offset = reader.read_fmt('3I')

        self.body_part_count, self.body_part_offset = reader.read_fmt('2I')
        self.local_attachment_count, self.local_attachment_offset = reader.read_fmt('2I')
        self.local_node_count, self.local_node_offset, self.local_node_name_offset = reader.read_fmt('3I')

        self.flex_desc_count, self.flex_desc_offset = reader.read_fmt('2I')
        self.flex_controller_count, self.flex_controller_offset = reader.read_fmt('2I')
        self.flex_rule_count, self.flex_rule_offset = reader.read_fmt('2I')

        self.ik_chain_count, self.ik_chain_offset = reader.read_fmt('2I')
        self.mouth_count, self.mouth_offset = reader.read_fmt('2I')
        self.local_pose_paramater_count, self.local_pose_parameter_offset = reader.read_fmt('2I')

        self.surface_prop = reader.read_source1_string(0)

        self.key_value_offset, self.key_value_size = reader.read_fmt('2I')
        self.local_ik_auto_play_lock_count, self.local_ik_auto_play_lock_offset = reader.read_fmt('2I')
        self.mass, self.contents = reader.read_fmt('fI')

        self.include_model_count, self.include_model_offset = reader.read_fmt('2I')
        self.virtual_model_pointer, self.anim_block_name_offset = reader.read_fmt('2I')
        self.anim_block_count, self.anim_block_offset = reader.read_fmt('2I')

        self.anim_block_model_pointer, self.bone_table_by_name_offset = reader.read_fmt('2I')

        self.vertex_base_pointer, self.index_base_pointer = reader.read_fmt('2I')

        self.directional_light_dot, self.root_lod, self.allowed_root_lod_count, self.unused = reader.read_fmt('4b')

        self.unused4 = reader.read_uint32()

        self.flex_controller_ui_count, self.flex_controller_ui_offset = reader.read_fmt('2I')
        self.vert_anim_fixed_point_scale, self.unused3 = reader.read_fmt('fI')
        self.studio_header2_offset, self.unused2 = reader.read_fmt('2I')

        self.source_bone_transform_count, self.source_bone_transform_offset = reader.read_fmt('2I')
        self.illum_position_attachment_index, self.max_eye_deflection = reader.read_fmt('If')
        self.linear_bone_offset, self.name_offset = reader.read_fmt('2I')

        if self.version > 47:
            self.bone_flex_driver_count, self.bone_flex_driver_offset = reader.read_fmt('2I')

        self.reserved = reader.read_fmt('56i')


class MdlHeaderV52(MdlHeaderV49):
    def __init__(self):
        super().__init__()
        self.maya_filename = ''

    def read(self, reader: ByteIO):
        self.id = reader.read_fourcc()
        self.version, self.checksum = reader.read_fmt('ii')
        self.store_value('mdl_version', self.version)
        self.name = reader.read_ascii_string(64)
        self.file_size = reader.read_uint32()
        assert self.file_size == reader.size()

        self.eye_position = reader.read_fmt('3f')
        self.illumination_position = reader.read_fmt('3f')
        self.hull_min = reader.read_fmt('3f')
        self.hull_max = reader.read_fmt('3f')

        self.view_bbox_min = reader.read_fmt('3f')
        self.view_bbox_max = reader.read_fmt('3f')

        self.flags = StudioHDRFlags(reader.read_uint32())

        self.bone_count, self.bone_offset = reader.read_fmt('2I')
        self.bone_controller_count, self.bone_controller_offset = reader.read_fmt('2I')

        self.hitbox_set_count, self.hitbox_set_offset = reader.read_fmt('2I')

        self.local_animation_count, self.local_animation_offset = reader.read_fmt('2I')
        self.local_sequence_count, self.local_sequence_offset = reader.read_fmt('2I')
        self.activity_list_version, self.events_indexed = reader.read_fmt('2I')

        self.texture_count, self.texture_offset = reader.read_fmt('2I')
        self.texture_path_count, self.texture_path_offset = reader.read_fmt('2I')
        self.skin_reference_count, self.skin_family_count, self.skin_family_offset = reader.read_fmt('3I')

        self.body_part_count, self.body_part_offset = reader.read_fmt('2I')
        self.local_attachment_count, self.local_attachment_offset = reader.read_fmt('2I')
        self.local_node_count, self.local_node_offset, self.local_node_name_offset = reader.read_fmt('3I')

        self.flex_desc_count, self.flex_desc_offset = reader.read_fmt('2I')
        self.flex_controller_count, self.flex_controller_offset = reader.read_fmt('2I')
        self.flex_rule_count, self.flex_rule_offset = reader.read_fmt('2I')

        self.ik_chain_count, self.ik_chain_offset = reader.read_fmt('2I')
        self.mouth_count, self.mouth_offset = reader.read_fmt('2I')
        self.local_pose_paramater_count, self.local_pose_parameter_offset = reader.read_fmt('2I')

        self.surface_prop = reader.read_source1_string(0)

        self.key_value_offset, self.key_value_size = reader.read_fmt('2I')
        self.local_ik_auto_play_lock_count, self.local_ik_auto_play_lock_offset = reader.read_fmt('2I')
        self.mass, self.contents = reader.read_fmt('fI')

        self.include_model_count, self.include_model_offset = reader.read_fmt('2I')
        self.virtual_model_pointer, self.anim_block_name_offset = reader.read_fmt('2I')
        self.anim_block_count, self.anim_block_offset = reader.read_fmt('2I')

        self.anim_block_model_pointer, self.bone_table_by_name_offset = reader.read_fmt('2I')

        self.vertex_base_pointer, self.index_base_pointer = reader.read_fmt('2I')

        self.directional_light_dot, self.root_lod, self.allowed_root_lod_count, self.unused = reader.read_fmt('4b')

        self.unused4 = reader.read_uint32()

        self.flex_controller_ui_count, self.flex_controller_ui_offset = reader.read_fmt('2I')
        self.vert_anim_fixed_point_scale, self.unused3 = reader.read_fmt('fI')
        self.studio_header2_offset = reader.read_uint32()

        self.maya_filename = reader.read_source1_string(0)

        self.source_bone_transform_count, self.source_bone_transform_offset = reader.read_fmt('2I')
        self.illum_position_attachment_index, self.max_eye_deflection = reader.read_fmt('If')
        self.linear_bone_offset, self.name_offset = reader.read_fmt('2I')

        if self.version > 47:
            self.bone_flex_driver_count, self.bone_flex_driver_offset = reader.read_fmt('2I')

        self.reserved = reader.read_fmt('56i')
