<template>
  <!-- Stage header -->
  <div class="flex items-center justify-between p-2 border border-base-300 bg-base-100">
    <h2 class="flex-1 font-semibold text-lg">{{ stage.title }}</h2>

    <!-- Stage options dropdown -->
    <div class="dropdown dropdown-right">
      <button
        tabindex="0"
        role="button"
        class="btn btn-sm btn-ghost"
        :disabled="
          kanbanMembersStore.currentUser && kanbanMembersStore.currentUser.role === 'viewer'
        "
      >
        ⋮
      </button>
      <ul
        tabindex="0"
        class="dropdown-content menu bg-base-200 border border-base-300 rounded-box w-48 p-2 shadow"
      >
        <li>
          <button class="flex gap-2 items-center" @click="openUpdateModal">
            <font-awesome-icon icon="fa-solid fa-pencil" />
            {{ $t('work.kanban.common.update_stage') }}
          </button>
        </li>
        <li>
          <button class="flex gap-2 items-center" @click="openInsertModal('before')">
            <font-awesome-icon icon="fa-solid fa-arrow-up" />
            {{ $t('work.kanban.common.insert_stage_before') }}
          </button>
        </li>
        <li>
          <button class="flex gap-2 items-center" @click="openInsertModal('after')">
            <font-awesome-icon icon="fa-solid fa-arrow-down" />
            {{ $t('work.kanban.common.insert_stage_after') }}
          </button>
        </li>
        <li>
          <button class="flex gap-2 items-center" @click="moveStage('right')">
            <font-awesome-icon icon="fa-solid fa-arrow-right" />
            {{ $t('work.kanban.common.move_stage_right') }}
          </button>
        </li>
        <li>
          <button class="flex gap-2 items-center" @click="moveStage('left')">
            <font-awesome-icon icon="fa-solid fa-arrow-left" />
            {{ $t('work.kanban.common.move_stage_left') }}
          </button>
        </li>
        <li>
          <button class="flex gap-2 items-center text-error" @click="openDeleteModal">
            <font-awesome-icon icon="fa-solid fa-trash" />
            {{ $t('work.kanban.common.delete_stage') }}
          </button>
        </li>
      </ul>
    </div>
  </div>

  <!-- BaseDialogs -->
  <BaseDialog
    v-model="updateModal"
    :title="$t('work.kanban.modals.update_stage_title.title')"
    :confirmText="$t('common.confirm')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmUpdateStage"
    @cancel="closeUpdateModal"
  >
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="errorStage">
          <h1 class="text-error mb-2">{{ errorStage }}</h1>
        </div>
      </Transition>
      <label for="stageTitle" class="label">{{
        $t('work.kanban.modals.update_stage_title.name')
      }}</label>
      <input
        type="text"
        class="input w-full"
        v-model="newStageTitle"
        :placeholder="$t('work.kanban.modals.update_stage_title.name_placeholder')"
      />
    </div>
  </BaseDialog>

  <BaseDialog
    v-model="insertModal"
    :title="$t('work.kanban.modals.insert_stage.title')"
    :confirmText="$t('common.create')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmInsertStage"
    @cancel="closeInsertModal"
  >
    <div class="flex flex-col gap-2 w-full">
      <Transition name="error-slide">
        <div v-if="errorStage">
          <h1 class="text-error mb-2">{{ errorStage }}</h1>
        </div>
      </Transition>
      <label for="stageTitle" class="label">
        {{ $t('work.kanban.modals.insert_stage.name') }}
      </label>
      <input
        type="text"
        class="input w-full"
        v-model="newStageTitle"
        :placeholder="$t('work.kanban.modals.insert_stage.name_placeholder')"
      />
    </div>
  </BaseDialog>

  <BaseDialog
    v-model="deleteModal"
    :title="$t('work.kanban.modals.delete_stage.title')"
    :confirmText="$t('common.delete')"
    :cancelText="$t('common.cancel')"
    @confirm="confirmDeleteStage"
  >
    {{ $t('work.kanban.modals.delete_stage.content') }}
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useKanbanStagesStore } from '@/stores/kanban/kanbanStages'
import { useKanbanBoardStore } from '@/stores/kanban/kanbanBoards'
import { useKanbanMembersStore } from '@/stores/kanban/kanbanMembers'

export default {
  name: 'kanbanStageTitle',
  props: {
    stage: { type: Object, required: true },
  },
  components: { BaseDialog },
  data() {
    return {
      updateModal: false,
      insertModal: false,
      deleteModal: false,
      newStageTitle: '',
      insertPosition: 'before',
      stagesStore: useKanbanStagesStore(),
      kanbanStore: useKanbanBoardStore(),
      kanbanMembersStore: useKanbanMembersStore(),
    }
  },
  methods: {
    // ===== Update Stage =====
    openUpdateModal() {
      this.newStageTitle = this.stage.title
      this.updateModal = true
    },
    closeUpdateModal() {
      this.newStageTitle = ''
      this.updateModal = false
      this.kanbanStore.clearError()
    },
    async confirmUpdateStage() {
      try {
        await this.stagesStore.updateStage({
          boardId: this.kanbanStore.selectedBoard.id,
          stageId: this.stage.id,
          title: this.newStageTitle.trim(),
        })
        this.updateModal = false
      } catch (err) {
        console.error('Failed to update stage:', err)
      }
    },

    // ===== Insert Relative Stage =====
    openInsertModal(position) {
      this.insertPosition = position
      this.newStageTitle = ''
      this.insertModal = true
    },
    closeInsertModal() {
      this.newStageTitle = ''
      this.insertModal = false
      this.stagesStore.clearError()
    },
    async confirmInsertStage() {
      try {
        await this.stagesStore.createStageRelative({
          boardId: this.kanbanStore.selectedBoard.id,
          title: this.newStageTitle.trim(),
          referenceStageId: this.stage.id,
          position: this.insertPosition,
        })
        this.insertModal = false
      } catch (err) {
        console.error(`Failed to insert stage ${this.insertPosition}:`, err)
      }
    },

    // ===== Move Stage =====
    async moveStage(direction) {
      try {
        await this.stagesStore.moveStage({
          boardId: this.kanbanStore.selectedBoard.id,
          stageId: this.stage.id,
          direction: direction === 'left' ? 'up' : 'down',
        })
      } catch (err) {
        console.error('Failed to move stage:', err)
      }
    },

    // ===== Delete Stage =====
    openDeleteModal() {
      this.deleteModal = true
    },
    async confirmDeleteStage() {
      try {
        await this.stagesStore.deleteStage({
          boardId: this.kanbanStore.selectedBoard.id,
          stageId: this.stage.id,
        })
        this.deleteModal = false
      } catch (err) {
        console.error('Failed to delete stage:', err)
      }
    },
  },
  computed: {
    errorStage() {
      return this.stagesStore.error
    },
  },
}
</script>
