<template>
  <div class="flex flex-col gap-5 p-5">
    <ProfileHeader v-if="user" :user="user"></ProfileHeader>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5" v-if="user">
      <UserInfoCard :user="user"></UserInfoCard>

      <div class="flex flex-col gap-5">
        <UserProgressCard v-for="(item, index) in progressItems" :key="index" v-bind="item"></UserProgressCard>
      </div>

      <UserModificationCard :actions="actions" @action-click="handleActionClick"></UserModificationCard>
    </div>

    <div v-else>Loading user...</div>

    <!-- Modals -->
    <BaseDialog v-model="openUsernameModal" :title="$t('modals.modify_user.new_username_title')"
      :confirm-text="$t('common.confirm')" :cancel-text="$t('common.cancel')" @confirm="submitUsernameChange">
      <div class="form-control flex flex-col gap-2 w-full">
        <label class="label">
          <span class="label-text">{{ $t('common.username') }}</span>
        </label>
        <input v-model="newUsername" type="text" :placeholder="$t('common.new_username')"
          class="input input-bordered w-full" />
      </div>
    </BaseDialog>

    <BaseDialog v-model="openEmailModal" :title="$t('modals.modify_user.new_email_title')"
      :confirm-text="$t('common.confirm')" :cancel-text="$t('common.cancel')" @confirm="submitEmailChange">
      <div class="form-control flex flex-col gap-2 w-full">
        <label class="label">
          <span class="label-text">{{ $t('common.email') }}</span>
        </label>
        <input v-model="newEmail" type="email" :placeholder="$t('common.new_email')"
          class="input input-bordered w-full" />
      </div>
    </BaseDialog>

    <BaseDialog v-model="openPasswordModal" :title="$t('modals.modify_user.new_password_title')"
      :confirm-text="$t('common.confirm')" :cancel-text="$t('common.cancel')"
      @confirm="submitPasswordChange">
      <div class="flex flex-col w-full gap-5">
        <p class="opacity-50">* {{ $t('common.if_google') }}</p>
        <div class="form-control flex flex-col gap-2 w-full">
          <label class="label">
            <span class="label-text">{{ $t('common.old_password') }}</span>
          </label>
          <input v-model="old_password" type="password" :placeholder="$t('common.password')"
            class="input input-bordered w-full" />
        </div>
        <div class="form-control flex flex-col gap-2 w-full">
          <label class="label">
            <span class="label-text">{{ $t('common.new_password') }}</span>
          </label>
          <input v-model="new_password" type="password" :placeholder="$t('common.password')"
            class="input input-bordered w-full" />
        </div>
      </div>
    </BaseDialog>
  </div>
</template>

<script>
import ProfileHeader from './ProfileHeader.vue'
import UserInfoCard from './UserInfoCard.vue'
import UserProgressCard from './UserProgressCard.vue'
import UserModificationCard from './UserModificationCard.vue'
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useUserStore } from '@/stores/user'

export default {
  name: 'UserProfileView',

  data() {
    return {
      openUsernameModal: false,
      openEmailModal: false,
      openPasswordModal: false,
      newUsername: '',
      newEmail: '',
      old_password: '',
      new_password: '',
    }
  },

  components: {
    ProfileHeader,
    UserInfoCard,
    UserProgressCard,
    UserModificationCard,
    BaseDialog,
  },

  computed: {
    user() {
      return useUserStore().user
    },

    progressItems() {
      return [
        { title: this.$t('cabinet.profile.kpi.tasks'), value: 78, max: 100, percent: 78, colorClass: 'text-success', progressClass: 'progress-success' },
        { title: this.$t('cabinet.profile.kpi.month_tasks'), value: 3, max: 5, percent: 60, colorClass: 'text-primary', progressClass: 'progress-primary' },
        { title: this.$t('cabinet.profile.kpi.week_activity'), value: 5, max: 7, percent: 71, colorClass: 'text-warning', progressClass: 'progress-warning' },
      ]
    },

    actions() {
      return [
        { key: 'username', title: this.$t('cabinet.profile.actions.edit_username') },
        { key: 'email', title: this.$t('cabinet.profile.actions.edit_email') },
        { key: 'password', title: this.$t('cabinet.profile.actions.change_password') },
      ]
    },
  },

  methods: {
    handleActionClick(key) {
      switch (key) {
        case 'username':
          this.openUsernameModal = true
          break
        case 'email':
          this.openEmailModal = true
          break
        case 'password':
          this.openPasswordModal = true
          break
      }
    },
    async submitUsernameChange() {

      const userStore = useUserStore()

      if (!this.newUsername || this.newUsername === '') return


      try {
        await userStore.changeUsername(this.newUsername)
        this.openUsernameModal = false
        this.newUsername = ''
      } catch (err) {
        console.error('Failed to change username:', err)
      }
    },
    async submitEmailChange() {

      const userStore = useUserStore()

      if (!this.newEmail || this.newEmail === '') return

      try {
        await userStore.changeEmail(this.newEmail)
        this.openEmailModal = false
        this.newEmail = ''
      } catch (err) {
        console.error('Failed to change email:', err)
      }
    },
    async submitPasswordChange() {

      const userStore = useUserStore()

      try {
        await userStore.changePassword(this.new_password, this.old_password)
        this.openPasswordModal = false
        this.old_password = ''
        this.new_password = ''
      } catch (err) {
        console.error('Failed to change password:', err)
      }
    },
  },

  mounted() {
    const userStore = useUserStore()
    if (!userStore.user) {
      userStore.fetchMe()
    }
  },
}
</script>

<style scoped></style>