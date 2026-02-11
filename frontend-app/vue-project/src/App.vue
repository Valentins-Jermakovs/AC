<template>
  <!-- Globālais Eye Rest Reminder -->
  <EyeRestReminder />

  <!-- Šeit tiek renderētas visas lapas -->
  <router-view></router-view>
</template>

<script>
import EyeRestReminder from './components/common/EyeRestReminder.vue'
import { useDocumentTitle } from './utils/useDocumentTitle'

export default {
  name: 'App',

  components: {
    EyeRestReminder,
  },

  setup() {
    // Ja tev ir hook dokumenta nosaukumam
    useDocumentTitle()
  },
}
</script>

<style scoped></style>
