<template>
  <div class="flex flex-col gap-5 p-5">

    <ProfileHeader :user="user"></ProfileHeader>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">

      <UserInfoCard :user="user"></UserInfoCard>

      <div class="flex flex-col gap-5">
        <UserProgressCard v-for="(item, index) in progressItems" :key="index" v-bind="item"></UserProgressCard>
      </div>

      <UserModificationCard :actions="actions"></UserModificationCard>
    </div>
  </div>
</template>

<script>
import ProfileHeader from './ProfileHeader.vue'
import UserInfoCard from './UserInfoCard.vue'
import UserProgressCard from './UserProgressCard.vue'
import UserModificationCard from './UserModificationCard.vue'

export default {
  name: 'UserProfileView',

  components: {
    ProfileHeader,
    UserInfoCard,
    UserProgressCard,
    UserModificationCard,
  },

  data() {
    return {
      user: {
        name: 'Valentīns Jermakovs',
        email: 'jermakovsvalentin@gmail.com',
        joined: '2025-06-20',
        role: 'Admin',
      },
    }
  },

  computed: {
    // Progress with translations
    progressItems() {
      let progressStatic = [
        { title: this.$t('cabinet.profile.kpi.tasks'), value: 78, max: 100, percent: 78, colorClass: 'text-success', progressClass: 'progress-success' },
        { title: this.$t('cabinet.profile.kpi.month_tasks'), value: 3, max: 5, percent: 60, colorClass: 'text-primary', progressClass: 'progress-primary' },
        { title: this.$t('cabinet.profile.kpi.week_activity'), value: 5, max: 7, percent: 71, colorClass: 'text-warning', progressClass: 'progress-warning' },
      ]

      return progressStatic
    },

    // Actions ar tulkojumiem
    actions() {
      let actionsStatic = [
        { title: this.$t('cabinet.profile.actions.edit_username') },
        { title: this.$t('cabinet.profile.actions.edit_email') },
        { title: this.$t('cabinet.profile.actions.change_password') },
      ]

      return actionsStatic
    },
  },
}
</script>


<style scoped></style>
