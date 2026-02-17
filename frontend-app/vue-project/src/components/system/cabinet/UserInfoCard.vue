<template>
  <!-- Card container for user contact information -->
  <div class="bg-base-200 border border-base-300 rounded-box p-5 flex flex-col gap-2">
    
    <!-- Section title -->
    <h3 class="text-lg font-semibold">
      {{ $t('cabinet.profile.contact_info') }}
    </h3>

    <!-- Email label -->
    <p>
      <strong>{{ $t('cabinet.profile.email') }}:</strong>
    </p>

    <!-- User email -->
    <p>{{ user.email }}</p>

    <!-- Roles label -->
    <p>
      <strong>{{ $t('cabinet.profile.roles') }}:</strong>
    </p>

    <!-- List of user roles -->
    <ul class="list-disc list-inside">
      <li v-for="(role, index) in user.roles" :key="index">
        {{ role }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'ProfileContactInfo',

  props: {
    // User object
    // Example:
    // {
    //   email: 'user@example.com',
    //   roles: ['admin', 'editor']
    // }
    user: {
      type: Object,
      required: true,
    },
  },
}
</script>

<style scoped></style>
