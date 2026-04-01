<template>
  <!-- MEMBERS -->
  <div class="flex-1 flex flex-col w-full h-full gap-3">
    <div class="w-full flex flex-col gap-4">
      <!-- HEADER -->
      <div class="w-full lg:h-16 flex flex-col lg:flex-row lg:items-center gap-3">
        <button class="btn btn-success lg:h-full" @click="openAddMemberModal">
          <font-awesome-icon icon="fa-solid fa-user-plus" />
          {{ $t('common.add_member') }}
        </button>

        <!-- SEARCH -->
        <div
          class="w-full h-full items-center flex flex-col sm:flex-row gap-2 border border-base-300 bg-base-200 p-2 wrap-break-word"
        >
          <input
            type="text"
            class="input w-full"
            :placeholder="$t('common.search')"
            v-model="eventParticipantsStore.searchQuery"
            :disabled="eventParticipantsStore.searchMode === 'all'"
          />

          <select
            class="bg-neutral text-neutral-content select select-bordered w-full sm:w-40"
            v-model="eventParticipantsStore.searchMode"
          >
            <option value="all">{{ $t('filters.all') }}</option>
            <option value="email">{{ $t('filters.by_email') }}</option>
          </select>

          <button
            class="btn btn-primary w-full sm:w-auto"
            @click="searchMembers"
            :disabled="
              eventParticipantsStore.searchMode !== 'all' &&
              eventParticipantsStore.searchQuery.length < 3
            "
          >
            <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
          </button>
        </div>
      </div>

      <!-- MEMBERS LIST -->
      <div
        class="w-full bg-base-200 border border-base-300 wrap-break-word p-2 sm:p-3 flex flex-col gap-3"
      >
        <div
          v-for="member in eventParticipantsStore.participants"
          :key="member.id"
          class="w-full flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3 bg-base-100 border border-base-300 wrap-break-word"
        >
          <!-- EMAIL -->
          <div
            class="flex items-center gap-2 flex-1 bg-base-200 p-3 border border-base-300 wrap-break-word break-all"
          >
            <font-awesome-icon icon="fa-solid fa-user" />

            {{ member.userEmail }}
          </div>

          <!-- ACTIONS -->
          <div class="dropdown dropdown-center md:dropdown-end">
            <div tabindex="0" role="button" class="btn w-full btn-neutral">⋮</div>

            <ul
              tabindex="0"
              class="dropdown-content menu bg-base-200 border border-base-300 wrap-break-word w-44 p-2 shadow"
            >
              <li>
                <button class="flex gap-2 text-error" @click="openDeleteMemberModal(member)">
                  <font-awesome-icon icon="fa-solid fa-trash" />
                  {{ $t('work.kanban.common.delete_member') }}
                </button>
              </li>
            </ul>
          </div>
        </div>

        <!-- EMPTY -->
        <div
          v-if="!eventParticipantsStore.loading && eventParticipantsStore.participants.length === 0"
          class="p-4 text-center text-base-content/60 flex items-center justify-center gap-2 flex-col"
        >
          <font-awesome-icon icon="fa-solid fa-users" class="text-3xl animate-bounce" />
          <progress class="progress w-1/3 progress-neutral" max="100"></progress>
          {{ $t('work.kanban.errors.members_not_found') }}
        </div>
      </div>

      <!-- FOOTER -->
      <div
        class="w-full flex flex-col sm:flex-row gap-3 sm:items-center bg-base-200 border border-base-300 wrap-break-word p-3 sm:px-4 sm:py-2"
      >
        <!-- LIMIT -->
        <div>
          <select
            class="select select-bordered w-full sm:w-24"
            v-model="eventParticipantsStore.meta.limit"
            @change="changeLimit($event.target.value)"
          >
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="30">30</option>
          </select>
        </div>

        <!-- META -->
        <div class="flex flex-col sm:flex-row gap-1 sm:gap-4 items-center md:items-start text-sm">
          <p>
            {{ $t('cabinet.admin.table_footer.total') }}
            <span class="font-semibold">
              {{ eventParticipantsStore.meta.total_items }}
            </span>
          </p>

          <p>
            {{ $t('cabinet.admin.table_footer.page') }}
            <span class="font-semibold">
              {{ eventParticipantsStore.meta.page }}/
              {{ eventParticipantsStore.meta.total_pages }}
            </span>
          </p>
        </div>

        <!-- PAGINATION -->
        <div class="flex flex-col md:flex-row gap-2 sm:ml-auto">
          <button
            class="btn w-full md:w-auto btn-neutral"
            @click="eventParticipantsStore.prevPage"
            :disabled="eventParticipantsStore.meta.page === 1"
          >
            <font-awesome-icon icon="fa-solid fa-arrow-left" />
          </button>

          <button
            class="btn w-full md:w-auto btn-neutral"
            @click="eventParticipantsStore.nextPage"
            :disabled="eventParticipantsStore.meta.page === eventParticipantsStore.meta.total_pages"
          >
            <font-awesome-icon icon="fa-solid fa-arrow-right" />
          </button>
        </div>
      </div>
    </div>
    <!-- Add member modal -->
    <base-dialog
      v-model="addMemberModal"
      :title="$t('calendar.modals.add_event_member.title')"
      :confirmText="$t('common.confirm')"
      :cancelText="$t('common.cancel')"
      @confirm="confirmAddMember"
      @cancel="closeAddMemberModal"
    >
      <div class="w-full flex flex-col gap-2">
        <Transition name="error-slide">
          <div v-if="error">
            <h1 class="text-error mb-2">{{ error }}</h1>
          </div>
        </Transition>
        <label for="memberEmail" class="label">
          {{ $t('work.kanban.modals.add_member.email') }}
        </label>
        <!-- Text input - member email -->
        <input
          type="email"
          class="input w-full"
          v-model="newMemberEmail"
          :placeholder="$t('work.kanban.modals.add_member.email_placeholder')"
        />
      </div>
    </base-dialog>

    <!-- Add member modal -->
    <base-dialog
      v-model="deleteMemberModal"
      :title="$t('calendar.modals.delete_event_member.title')"
      :confirmText="$t('common.confirm')"
      :cancelText="$t('common.cancel')"
      @confirm="confirmDeleteMember"
      @cancel="closeDeleteMemberModal"
    >
      <div class="w-full flex flex-col gap-2">
        <Transition name="error-slide">
          <div v-if="memberError">
            <h1 class="text-error mb-2">{{ memberError }}</h1>
          </div>
        </Transition>
        <p>{{ $t('calendar.modals.delete_event_member.content') }}</p>
      </div>
    </base-dialog>
  </div>
</template>

<script>
import { useEventParticipantsStore } from '@/stores/eventParticipants'
import { useEventsStore } from '@/stores/events'
import { useAdminStore } from '@/stores/admin'

import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'EventMembers',

  components: { BaseDialog },
  data() {
    return {
      eventParticipantsStore: useEventParticipantsStore(),
      eventsStore: useEventsStore(),
      addMemberModal: false,
      deleteMemberModal: false,
      newMemberEmail: '',
      adminStore: useAdminStore(),
      member: {},
    }
  },

  computed: {
    error() {
      return this.adminStore.error
    },
    memberError() {
      return this.eventParticipantsStore.error
    },
  },

  mounted() {
    this.eventParticipantsStore.fetchParticipants()
  },

  methods: {
    async searchMembers() {
      // reset page when new search starts
      this.eventParticipantsStore.meta.page = 1

      if (this.eventParticipantsStore.searchMode === 'all') {
        await this.eventParticipantsStore.fetchParticipants()
      }

      if (this.eventParticipantsStore.searchMode === 'email') {
        await this.eventParticipantsStore.fetchParticipantsByEmail()
      }
    },

    async changeLimit(limit) {
      await this.eventParticipantsStore.setLimit(limit)
    },

    async openAddMemberModal() {
      this.addMemberModal = true
    },
    closeAddMemberModal() {
      this.adminStore.clearError()
      this.eventParticipantsStore.clearError()
      this.addMemberModal = false
      this.newMemberEmail = ''
    },
    async confirmAddMember() {
      if (!this.newMemberEmail) {
        this.adminStore.error = 'Email is required'
        return
      }

      // validate email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(this.newMemberEmail)) {
        this.adminStore.error = 'Invalid email format'
        return
      }

      try {
        // send email to auth server - /users/email/{email}
        await this.adminStore.getUserByEmail(this.newMemberEmail)

        const addedUser = this.adminStore.userByEmail

        const payload = {
          userEmail: addedUser.email,
          userId: String(addedUser.id),
          eventId: this.eventParticipantsStore.selectedEvent.id,
        }

        await this.eventParticipantsStore.createParticipant(payload)

        this.addMemberModal = false
        this.newMemberEmail = ''
      } catch (err) {
        console.error('Failed to add member:', err)
      }
    },
    async openDeleteMemberModal(member) {
      this.deleteMemberModal = true
      this.member = member
    },
    closeDeleteMemberModal() {
      this.deleteMemberModal = false
      this.eventParticipantsStore.clearError()
    },
    async confirmDeleteMember() {
      const payload = {
        userId: this.member.userId,
        eventId: this.eventParticipantsStore.selectedEvent.id,
      }
      try {
        await this.eventParticipantsStore.removeParticipant(payload.eventId, payload.userId)
        this.deleteMemberModal = false
      } catch (err) {
        console.error('Failed to delete member:', err)
      }
    },
  },
}
</script>

<style scoped></style>
