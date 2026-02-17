<template>
  <!-- Card container for profile actions -->
  <div class="bg-base-200 border border-base-300 rounded-box p-5 flex flex-col gap-3">
    
    <!-- Section title -->
    <h3 class="text-lg font-semibold mb-2">
      {{ $t('cabinet.profile.actions.title') }}
    </h3>

    <!-- Render action buttons -->
    <button
      v-for="(action, index) in actions"
      :key="index"
      class="btn btn-neutral w-full justify-start hover:btn-secondary transition-all duration-300"
      @click="$emit('action-click', action.key)"
    >
      {{ action.title }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'ProfileActionsCard',

  props: {
    // List of action objects
    // Example:
    // [
    //   { title: 'Edit Profile', key: 'edit' },
    //   { title: 'Change Password', key: 'password' }
    // ]
    actions: {
      type: Array,
      required: true,
    },
  },
}
</script>

<style scoped></style>
