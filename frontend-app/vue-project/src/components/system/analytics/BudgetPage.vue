<template>
  <div class="h-full bg-base-100 p-6 flex flex-col gap-6">
    <!-- HEADER -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-xl font-bold">{{ $t('finances.budgets.title') }}</h1>
        <p class="text-sm opacity-60">
          {{ budgetStore.yearAndMonth }}
        </p>
      </div>

      <button class="btn btn-primary btn-sm" @click="openCreate">
        <font-awesome-icon icon="fa-solid fa-pencil"></font-awesome-icon>
        {{ $t('finances.budgets.new_budget') }}
      </button>
    </div>

    <!-- STATS -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="card rounded-none bg-base-200 border border-base-300 p-4">
        <div class="text-sm opacity-60">{{ $t('finances.budgets.total_budgets') }}</div>
        <div class="text-2xl font-bold">{{ budgets.length }}</div>
      </div>

      <div class="card rounded-none bg-base-200 border border-base-300 p-4">
        <div class="text-sm opacity-60">{{ $t('finances.budgets.total_limit') }}</div>
        <div class="text-2xl font-bold">€{{ totalLimit }}</div>
      </div>

      <div class="card rounded-none bg-base-200 border border-base-300 p-4">
        <div class="text-sm opacity-60">{{ $t('finances.budgets.month') }}</div>
        <div class="text-2xl font-bold">{{ budgetStore.yearAndMonth }}</div>
      </div>
    </div>

    <!-- CHART -->
    <div class="card rounded-none bg-base-200 border border-base-300 p-4 h-80 flex flex-col">
      <div class="font-semibold mb-2">{{ $t('finances.budgets.budget_limits') }}</div>
      <div class="flex-1" v-if="budgets.length > 0">
        <canvas ref="budgetChart"></canvas>
      </div>
      <div v-else class="flex flex-col items-center justify-center gap-2 h-full text-base-content/70">
        <font-awesome-icon icon="fa-solid fa-chart-bar" class="text-4xl animate-bounce" />
        <p class="text-lg">{{ $t('finances.budgets.no_budgets') }}</p>
      </div>
    </div>

      <!-- MOBILE CARDS -->
  <div class="flex flex-col gap-3 md:hidden">
    <div
      v-for="b in budgets"
      :key="b.id"
      class="card bg-base-200 rounded-none border border-base-300 p-3"
    >
      <!-- TOP -->
      <div class="flex justify-between items-center">
        <span class="badge badge-neutral">
          {{ b.category }}
        </span>

        <span class="text-sm opacity-70">
          {{ b.month }}
        </span>
      </div>

      <!-- LIMIT -->
      <div class="mt-2 font-semibold text-right text-lg">
        €{{ b.planned_amount }}
      </div>

      <!-- ACTIONS -->
      <div class="flex gap-2 mt-3">
        <button class="btn btn-xs btn-info flex-1" @click="openUpdate(b)">
          {{ $t('finances.budgets.actions.edit') }}
        </button>

        <button class="btn btn-xs btn-error flex-1" @click="openDelete(b)">
          {{ $t('finances.budgets.actions.delete') }}
        </button>
      </div>
    </div>

    <!-- EMPTY -->
    <div v-if="!budgets.length" class="text-center opacity-60 py-6 flex items-center justify-center">
      <font-awesome-icon icon="fa-solid fa-wallet" class="text-3xl animate-bounce" />
      <p class="text-error animate-bounce">{{ $t('finances.budgets.no_budgets') }}</p>
    </div>
  </div>


    <!-- TABLE -->
    <div class="card hidden md:block rounded-none bg-base-200 border border-base-300 p-4">
      <div class="font-semibold mb-3">{{ $t('finances.budgets.budgets') }}</div>

      <div class="overflow-x-auto">
        <table class="table table-sm w-full">
          <thead>
            <tr class="opacity-70">
              <th>{{ $t('finances.budgets.category') }}</th>
              <th>{{ $t('finances.budgets.limit') }}</th>
              <th>{{ $t('finances.budgets.month') }}</th>
              <th class="text-right">{{ $t('finances.budgets.table_actions') }}</th>
            </tr>
          </thead>

          <tbody class="bg-base-100">
            <tr v-for="b in budgets" :key="b.id">
              <td>
                <span class="badge badge-neutral">
                  {{ b.category }}
                </span>
              </td>

              <td class="font-medium">€{{ b.planned_amount }}</td>

              <td class="opacity-70">
                {{ b.month }}
              </td>

              <td class="text-right">
                <div class="flex justify-end gap-2">
                  <button class="btn btn-xs btn-info" @click="openUpdate(b)">{{ $t('finances.budgets.actions.edit')
                    }}</button>
                  <button class="btn btn-xs btn-error" @click="openDelete(b)">{{ $t('finances.budgets.actions.delete')
                    }}</button>
                </div>
              </td>
            </tr>

            <tr v-if="!budgets.length">
              <td colspan="4" class="text-center opacity-60 py-6">
                <font-awesome-icon icon="fa-solid fa-wallet" class="text-3xl animate-bounce" />
                <p class="text-error animate-bounce">{{ $t('finances.budgets.no_budgets') }}</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>



    <!-- CREATE / UPDATE MODAL -->
    <BaseDialog v-model="modal"
      :title="editing ? $t('finances.budgets.modals.edit_budget.title') : $t('finances.budgets.modals.create_budget.title')"
      :confirmText="editing ? $t('common.confirm') : $t('common.create')" :cancelText="$t('common.cancel')"
      @confirm="saveBudget" @cancel="closeModal">
      <div class="flex flex-col gap-2 w-full">
        <Transition name="error-slide">
          <div v-if="error" class="mb-4">
            <div class="text-error">
              <span>{{ error }}</span>
            </div>
          </div>
        </Transition>
        <label for="category" class="label">{{ $t('finances.budgets.modals.edit_budget.category') }}</label>
        <input v-model="form.category" class="input input-bordered w-full"
          :placeholder="$t('finances.budgets.modals.edit_budget.category_placeholder')" />
        <label for="planned_amount" class="label">{{ $t('finances.budgets.modals.edit_budget.limit') }}</label>
        <input v-model.number="form.planned_amount" type="number" class="input input-bordered w-full"
          :placeholder="$t('finances.budgets.modals.edit_budget.limit_placeholder')" />
        <label for="month" class="label">{{ $t('finances.budgets.modals.edit_budget.month') }}</label>
        <input v-model="form.month" class="input input-bordered w-full" placeholder="YYYY-MM" />
      </div>
    </BaseDialog>

    <!-- DELETE -->
    <BaseDialog v-model="deleteModal" :title="$t('finances.budgets.modals.delete_budget.title')"
      :confirmText="$t('common.delete')" :cancelText="$t('common.cancel')" @confirm="deleteBudget"
      @cancel="closeDeleteModal">
      <Transition name="error-slide">
        <div v-if="error" class="mb-4">
          <div class="alert alert-error">
            <span>{{ error }}</span>
          </div>
        </div>
      </Transition>
      <p>{{ $t('finances.budgets.modals.delete_budget.content') }}</p>
    </BaseDialog>

    <LoadingScreen v-if="budgetStore.loading"></LoadingScreen>
  </div>
</template>

<script>
import { useBudgetStore } from '@/stores/budget'
import { Chart } from 'chart.js/auto'
import BaseDialog from '@/components/common/BaseDialog.vue'
import LoadingScreen from '@/components/common/LoadingScreen.vue';

export default {
  components: { BaseDialog, LoadingScreen },

  data() {
    return {
      budgetStore: useBudgetStore(),

      modal: false,
      deleteModal: false,
      editing: false,
      selected: null,
      error: null,

      form: {
        category: '',
        planned_amount: 0,
        month: '',
      },

      chartInstance: null,
    }
  },

  async mounted() {
    await this.budgetStore.fetchBudgets()
    this.updateCharts()
  },

  computed: {
    budgets() {
      return this.budgetStore.budgets
    },

    totalLimit() {
      return this.budgets.reduce((s, b) => s + b.planned_amount, 0)
    },
  },

  methods: {
    async refresh() {
      await this.budgetStore.fetchBudgets()
      this.updateCharts()
    },

    openCreate() {
      this.editing = false
      this.form = { category: '', planned_amount: 0, month: '' }
      this.error = null
      this.modal = true
    },

    openUpdate(b) {
      this.editing = true
      this.selected = b
      this.form = {
        category: b.category,
        planned_amount: b.planned_amount,
        month: b.month,
      }
      this.error = null
      this.modal = true
    },

    async saveBudget() {
      try {
        this.error = null
        const payload = {
          category: this.form.category,
          month: this.form.month,
          planned_amount: this.form.planned_amount,
        }

        if (this.editing) {
          await this.budgetStore.updateBudget(this.selected.id, payload)
        } else {
          await this.budgetStore.createBudget(payload)
        }

        if (this.budgetStore.error) {
          this.error = this.budgetStore.error
          return
        }

        this.modal = false
        await this.refresh()
      } catch (err) {
        this.error = this.budgetStore.error || err.message || 'Failed to save budget'
        console.error('Error saving budget:', err)
      }
    },

    closeModal() {
      this.modal = false
      this.budgetStore.clearError()
    },

    openDelete(b) {
      this.selected = b
      this.error = null
      this.deleteModal = true
    },

    async deleteBudget() {
      try {
        this.error = null
        await this.budgetStore.deleteBudget(this.selected.id)

        if (this.budgetStore.error) {
          this.error = this.budgetStore.error
          return
        }

        this.deleteModal = false
        await this.refresh()
      } catch (err) {
        this.error = this.budgetStore.error || err.message || 'Failed to delete budget'
        console.error('Error deleting budget:', err)
      }
    },

    closeDeleteModal() {
      this.deleteModal = false
      this.error = null
    },

    renderChart() {
      if (this.chartInstance) this.chartInstance.destroy()

      // Guard: ensure the canvas ref exists
      if (!this.$refs.budgetChart) return

      const ctx = this.$refs.budgetChart.getContext('2d')

      this.chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.budgets.map((b) => b.category),
          datasets: [
            {
              label: this.$t('finances.budgets.limit'),
              data: this.budgets.map((b) => b.planned_amount),
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animations: {
            numbers: {
              duration: 2000,
              easing: 'easeInOutCubic'
            }
          },
          plugins: {
            tooltip: {
              enabled: true,
              backgroundColor: 'rgba(0, 0, 0, 1)',
              padding: 20,
              boxPadding: 10,
              cornerRadius: 0,
              titleFont: { size: 14, weight: '600' },
              bodyFont: { size: 16 }
            },
          },
        },
      })
    },

    updateCharts() {
      this.$nextTick(() => {
        requestAnimationFrame(() => {
          this.renderChart()
        })
      })
    },
  },
}
</script>
