<template>
  <div class="flex items-center gap-5 p-5 bg-base-200 border border-base-300 rounded-box">
    <font-awesome-icon icon="user-circle" class="text-6xl" />
    <div class="flex flex-col gap-1">
      <h2 class="text-2xl font-semibold">{{ user.username }}</h2>
      <p class="text-sm text-base-content/50">
        {{ $t('cabinet.profile.created_at') }}: {{ user.created_at }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
    },
  },
}
</script>


<style scoped></style>
