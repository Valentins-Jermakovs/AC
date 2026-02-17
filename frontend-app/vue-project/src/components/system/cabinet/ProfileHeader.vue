<template>
  <!-- Container for user profile header -->
  <div class="flex items-center gap-5 p-5 bg-base-200 border border-base-300 rounded-box">
    
    <!-- User avatar icon -->
    <font-awesome-icon 
      icon="user-circle" 
      class="text-6xl" 
    />

    <!-- User info: username and creation date -->
    <div class="flex flex-col gap-1">
      
      <!-- Display username -->
      <h2 class="text-2xl font-semibold">
        {{ user.username }}
      </h2>

      <!-- Display account creation date with label from translation -->
      <p class="text-sm text-base-content/50">
        {{ $t('cabinet.profile.created_at') }}: {{ user.created_at }}
      </p>
    </div>

  </div>
</template>

<script>
export default {
  // Props passed from parent component
  props: {
    user: {
      type: Object, // expects an object with user data (username, created_at, etc.)
    },
  },
}
</script>

<style scoped>
/* Scoped styling so it applies only to this component */
/* Currently empty, styling handled via TailwindCSS classes in template */
</style>
