<template>
  <div class="bg-base-200 border border-base-300 rounded-box p-5 flex flex-col gap-2">
    <h3 class="text-lg font-semibold">{{ $t('cabinet.profile.contact_info') }}</h3>
    <p>
      <strong>{{ $t('cabinet.profile.email') }}:</strong>
    </p>
    <p> {{ user.email }}</p>
    <p>
      <strong>{{ $t('cabinet.profile.roles') }}:</strong>
    </p>
    <ul class="list-disc list-inside">
      <li v-for ="(role, index) in user.roles" :key="index">
        {{ role }}
      </li>
    </ul>
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
