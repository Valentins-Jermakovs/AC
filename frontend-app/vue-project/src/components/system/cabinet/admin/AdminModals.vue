<template>
  <!-- Add role modal -->
  <BaseDialog
    :model-value="addRoleModal"
    :title="$t('modals.add_role.title')"
    :cancel-text="$t('common.cancel')"
    :confirm-text="$t('common.confirm')"
    @confirm="$emit('add-role')"
    @cancel="$emit('update:add-role-modal', false)"
  >
    <div class="flex flex-col gap-2 w-full">
      <label>{{ $t('modals.add_role.label') }}</label>
      <select :value="selectedAddRole" @change="onAddRoleChange" class="select select-bordered w-full">
        <option value="2">Admin</option>
        <option value="3">Developer</option>
        <option value="4">Manager</option>
        <option value="5">Support</option>
        <option value="6">Content Manager</option>
      </select>
    </div>
  </BaseDialog>

  <!-- Remove role modal -->
  <BaseDialog
    :model-value="removeRoleModal"
    :title="$t('modals.remove_role.title')"
    :cancel-text="$t('common.cancel')"
    :confirm-text="$t('common.confirm')"
    @confirm="$emit('remove-role')"
    @cancel="$emit('update:remove-role-modal', false)"
  >
    <div class="flex flex-col gap-2 w-full">
      <label>{{ $t('modals.remove_role.label') }}</label>
      <select :value="selectedRemoveRole" @change="onRemoveRoleChange" class="select select-bordered w-full">
        <option value="2">Admin</option>
        <option value="3">Developer</option>
        <option value="4">Manager</option>
        <option value="5">Support</option>
        <option value="6">Content Manager</option>
      </select>
    </div>
  </BaseDialog>

  <!-- Change activity modal -->
  <BaseDialog
    :model-value="changeActivityModal"
    :title="$t('modals.change_activity.title')"
    :cancel-text="$t('common.cancel')"
    :confirm-text="$t('common.confirm')"
    @confirm="$emit('change-activity')"
    @cancel="$emit('update:change-activity-modal', false)"
  >
    <div class="flex flex-col gap-2 w-full">
      <label>{{ $t('modals.change_activity.label') }}</label>
      <select :value="selectedActivityStatus" @change="onActivityStatusChange" class="select select-bordered w-full">
        <option value="active">{{ $t('modals.change_activity.active') }}</option>
        <option value="blocked">{{ $t('modals.change_activity.blocked') }}</option>
      </select>
    </div>
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'AdminModals',
  components: { BaseDialog },
  props: {
    addRoleModal: Boolean,
    removeRoleModal: Boolean,
    changeActivityModal: Boolean,
    selectedAddRole: Number,
    selectedRemoveRole: Number,
    selectedActivityStatus: String,
  },
  emits: [
    'add-role',
    'remove-role',
    'change-activity',
    'update:add-role-modal',
    'update:remove-role-modal',
    'update:change-activity-modal',
    'update:selected-add-role',
    'update:selected-remove-role',
    'update:selected-activity-status'
  ],
  methods: {
    onAddRoleChange(e) {
      this.$emit('update:selected-add-role', Number(e.target.value))
    },
    onRemoveRoleChange(e) {
      this.$emit('update:selected-remove-role', Number(e.target.value))
    },
    onActivityStatusChange(e) {
      this.$emit('update:selected-activity-status', e.target.value)
    },
  },
}
</script>

<style scoped></style>
