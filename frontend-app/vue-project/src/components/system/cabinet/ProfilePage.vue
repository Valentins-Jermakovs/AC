<template>
  <div class="flex flex-col gap-5 p-5">
    <ProfileHeader v-if="user" :user="user"></ProfileHeader>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5" v-if="user">
      <UserInfoCard :user="user"></UserInfoCard>

      <div class="flex flex-col gap-5">
        <UserProgressCard
          v-for="(item, index) in progressItems"
          :key="index"
          v-bind="item"
        ></UserProgressCard>
      </div>

      <UserModificationCard
        :actions="actions"
        @action-click="handleActionClick"
      ></UserModificationCard>
    </div>

    <LoadingScreen v-else></LoadingScreen>

    <!-- Modals -->
    <BaseDialog
      v-model="openUsernameModal"
      :title="$t('modals.modify_user.new_username_title')"
      :confirm-text="$t('common.confirm')"
      :cancel-text="$t('common.cancel')"
      @confirm="submitUsernameChange"
    >
      <div class="flex flex-col w-full gap-5">
        <Transition name="error-slide">
          <div v-if="error" class="overflow-hidden">
            <h1 class="text-red-500 mb-2">
              {{ error }}
            </h1>
          </div>
        </Transition>
        <div class="form-control flex flex-col gap-2 w-full">
          <label class="label">
            <span class="label-text">{{ $t('common.username') }}</span>
          </label>
          <input
            v-model="newUsername"
            type="text"
            :placeholder="$t('common.new_username')"
            class="input input-bordered w-full"
          />
        </div>
      </div>
    </BaseDialog>

    <BaseDialog
      v-model="openEmailModal"
      :title="$t('modals.modify_user.new_email_title')"
      :confirm-text="$t('common.confirm')"
      :cancel-text="$t('common.cancel')"
      @confirm="submitEmailChange"
    >
      <div class="flex flex-col w-full gap-5">
        <Transition name="error-slide">
          <div v-if="error" class="overflow-hidden">
            <h1 class="text-red-500 mb-2">
              {{ error }}
            </h1>
          </div>
        </Transition>
        <div class="form-control flex flex-col gap-2 w-full">
          <label class="label">
            <span class="label-text">{{ $t('common.email') }}</span>
          </label>
          <input
            v-model="newEmail"
            type="email"
            :placeholder="$t('common.new_email')"
            class="input input-bordered w-full"
          />
        </div>
      </div>
    </BaseDialog>

    <BaseDialog
      v-model="openPasswordModal"
      :title="$t('modals.modify_user.new_password_title')"
      :confirm-text="$t('common.confirm')"
      :cancel-text="$t('common.cancel')"
      @confirm="submitPasswordChange"
    >
      <div class="flex flex-col w-full gap-5">
        <Transition name="error-slide">
          <div v-if="error" class="overflow-hidden">
            <h1 class="text-red-500 mb-2">
              {{ error }}
            </h1>
          </div>
        </Transition>
        <p class="opacity-50">* {{ $t('common.if_google') }}</p>
        <div class="form-control flex flex-col gap-2 w-full">
          <label class="label">
            <span class="label-text">{{ $t('common.old_password') }}</span>
          </label>
          <input
            v-model="old_password"
            type="password"
            :placeholder="$t('common.password')"
            class="input input-bordered w-full"
          />
        </div>
        <div class="form-control flex flex-col gap-2 w-full">
          <label class="label">
            <span class="label-text">{{ $t('common.new_password') }}</span>
          </label>
          <input
            v-model="new_password"
            type="password"
            :placeholder="$t('common.password')"
            class="input input-bordered w-full"
          />
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
import LoadingScreen from '@/components/common/LoadingScreen.vue'

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
    LoadingScreen,
  },

  computed: {
    user() {
      return this.userStore.user
    },

    progressItems() {
      return [
        {
          title: this.$t('cabinet.profile.kpi.tasks'),
          value: 78,
          max: 100,
          percent: 78,
          colorClass: 'text-success',
          progressClass: 'progress-success',
        },
        {
          title: this.$t('cabinet.profile.kpi.month_tasks'),
          value: 3,
          max: 5,
          percent: 60,
          colorClass: 'text-primary',
          progressClass: 'progress-primary',
        },
        {
          title: this.$t('cabinet.profile.kpi.week_activity'),
          value: 5,
          max: 7,
          percent: 71,
          colorClass: 'text-warning',
          progressClass: 'progress-warning',
        },
      ]
    },

    userStore() {
      return useUserStore()
    },
    error() {
      return this.userStore.error
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
    closeModal(modalName) {
      switch (modalName) {
        case 'username':
          this.openUsernameModal = false
          this.userStore.error = ''
          break
        case 'email':
          this.openEmailModal = false
          this.userStore.error = ''
          break
        case 'password':
          this.openPasswordModal = false
          this.userStore.error = ''
          break
        default:
          break
      }
    },
    handleActionClick(key) {
      switch (key) {
        case 'username':
          this.openUsernameModal = true
          this.userStore.clearError()
          break
        case 'email':
          this.openEmailModal = true
          this.userStore.clearError()
          break
        case 'password':
          this.openPasswordModal = true
          this.userStore.clearError()
          break
      }
    },
    async submitUsernameChange() {
      if (!this.newUsername || this.newUsername === '') return

      try {
        await this.userStore.changeUsername(this.newUsername)
        this.openUsernameModal = false
        this.newUsername = ''
      } catch (err) {
        console.error('Failed to change username:', err)
      }
    },
    async submitEmailChange() {
      if (!this.newEmail || this.newEmail === '') return

      try {
        await this.userStore.changeEmail(this.newEmail)
        this.openEmailModal = false
        this.newEmail = ''
      } catch (err) {
        console.error('Failed to change email:', err)
      }
    },
    async submitPasswordChange() {
      try {
        await this.userStore.changePassword(this.new_password, this.old_password)
        this.openPasswordModal = false
        this.old_password = ''
        this.new_password = ''
      } catch (err) {
        console.error('Failed to change password:', err)
      }
    },
  },

  mounted() {
    if (!this.userStore.user) {
      this.userStore.fetchMe()
    }
  },
}
</script>

<style scoped>
.error-slide-enter-active,
.error-slide-leave-active {
  transition: all 0.4s ease;
}

.error-slide-enter-from,
.error-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}

.error-slide-enter-to,
.error-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
  max-height: 100px;
}
</style>
