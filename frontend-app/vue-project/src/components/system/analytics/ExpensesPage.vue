<template>
  <div class="h-full bg-base-100 p-4 flex flex-col gap-4">
    <!-- CARDS -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="card rounded-none border border-base-300 bg-base-200 p-4">
        <div class="text-sm opacity-70">{{ $t('finances.expenses.total_spent') }}</div>
        <div class="text-2xl font-bold">€{{ total }}</div>
      </div>

      <div class="card rounded-none border border-base-300 bg-base-200 p-4">
        <div class="text-sm opacity-70">{{ $t('finances.expenses.transactions') }}</div>
        <div class="text-2xl font-bold">
          {{ expenseStore.meta.total_expenses }}
        </div>
      </div>

      <div class="card rounded-none border border-base-300 bg-base-200 p-4">
        <div class="text-sm opacity-70">{{ $t('finances.expenses.top_category') }}</div>
        <div class="text-2xl font-bold">
          {{ topCategory?.category || '-' }}
        </div>
      </div>

      <div class="card rounded-none border border-base-300 bg-base-200 p-4">
        <div class="text-sm opacity-70">{{ $t('finances.expenses.today_spent') }}</div>
        <div class="text-2xl font-bold">€{{ todayTotal }}</div>
      </div>
    </div>

    <!-- CHARTS -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 flex-1">
      <div class="card rounded-none border border-base-300 bg-base-200 p-4 h-80 flex flex-col">
        <div class="font-semibold mb-2">{{ $t('finances.expenses.category_charts') }}</div>

        <div class="flex-1 relative">
          <canvas ref="categoryChart"></canvas>
        </div>
      </div>

      <div class="card rounded-none border border-base-300 bg-base-200 p-4 h-80 flex flex-col">
        <div class="font-semibold mb-2">{{ $t('finances.expenses.timeline') }}</div>

        <div class="flex-1 relative">
          <canvas ref="timelineChart"></canvas>
        </div>
      </div>
    </div>

    <div class="flex justify-end">
      <button class="btn btn-primary btn-sm" @click="openCreate">
        <font-awesome-icon icon="fa-solid fa-pencil"></font-awesome-icon>
        {{ $t('finances.expenses.new_expense') }}
      </button>
    </div>

    <!-- EXPENSE LIST -->
    <div class="card rounded-none border border-base-300 bg-base-200 p-4 flex flex-col gap-3">
      <div class="flex justify-between items-center">
        <div class="font-semibold">{{ $t('finances.expenses.expenses') }}</div>

        <div class="text-sm opacity-70">
          {{ $t('finances.expenses.page') }} {{ expenseStore.meta.page }} / {{ expenseStore.meta.total_pages }}
        </div>
      </div>

      <!-- TABLE -->
      <div class="overflow-auto flex-1">
        <table class="table table-sm w-full">
          <thead>
            <tr>
              <th>{{ $t('finances.expenses.date') }}</th>
              <th>{{ $t('finances.expenses.category') }}</th>
              <th>{{ $t('finances.expenses.description') }}</th>
              <th class="text-right">{{ $t('finances.expenses.amount') }}</th>
              <th class="text-right">{{ $t('finances.expenses.table_actions') }}</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="e in expenseStore.expenses" :key="e.id">
              <td class="whitespace-nowrap">
                {{ formatDate(e.date) }}
              </td>

              <td>
                <span class="badge badge-outline">
                  {{ e.category }}
                </span>
              </td>

              <td class="max-w-50 truncate">
                {{ e.description }}
              </td>

              <td class="text-right font-semibold">€{{ e.amount }}</td>

              <td class="text-right">
                <div class="flex gap-2 justify-end">
                  <button class="btn btn-xs btn-info" @click="openUpdate(e)">{{ $t('finances.expenses.actions.edit') }}</button>

                  <button class="btn btn-xs btn-error" @click="openDelete(e)">{{ $t('finances.expenses.actions.delete') }}</button>
                </div>
              </td>
            </tr>

            <tr v-if="!expenseStore.expenses.length">
              <td colspan="5" class="text-center opacity-60 py-6">No expenses found</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- PAGINATION -->
      <div class="flex justify-between items-center pt-2">
        <button class="btn btn-sm" :disabled="expenseStore.meta.page <= 1" @click="prevPage">
          {{ $t('finances.expenses.prev') }}
        </button>

        <div class="text-sm opacity-70">
          {{ $t('finances.expenses.total') }} {{ expenseStore.meta.total_expenses }}
        </div>

        <button
          class="btn btn-sm"
          :disabled="expenseStore.meta.page >= expenseStore.meta.total_pages"
          @click="nextPage"
        >
          {{ $t('finances.expenses.next') }}
        </button>
      </div>
    </div>

    <!-- Delete Modal -->
    <BaseDialog
      v-model="deleteModal"
      @confirm="deleteExpense"
      @cancel="closeDelete"
      :confirmText="$t('common.create')"
      :cancelText="$t('common.cancel')"
      :title="$t('finances.expenses.modals.delete_expense.title')"
    >
      <p>{{ $t('finances.expenses.modals.delete_expense.content') }}</p>
    </BaseDialog>
    <!-- Update Modal-->
    <BaseDialog
      v-model="updateModal"
      @confirm="updateExpense"
      @cancel="closeUpdate"
      :confirmText="$t('common.create')"
      :cancelText="$t('common.cancel')"
      :title="$t('finances.expenses.modals.edit_expense.title')"
    >
      <!-- Inputs: (amount, category, date, description) -->
      <div class="flex flex-col gap-2 w-full">
        <label for="amount" class="label">{{ $t('finances.expenses.modals.edit_expense.amount') }}</label>
        <input
          type="number"
          v-model="expense.amount"
          class="input w-full"
          :placeholder="$t('finances.expenses.modals.edit_expense.amount_placeholder')"
          required
        />

        <label for="category" class="label">{{ $t('finances.expenses.modals.edit_expense.category') }}</label>
        <input
          type="text"
          v-model="expense.category"
          class="input w-full"
          :placeholder="$t('finances.expenses.modals.edit_expense.category_placeholder')"
          required
        />

        <label for="date" class="label">{{ $t('finances.expenses.modals.edit_expense.date') }}</label>
        <input
          type="date"
          v-model="expense.date"
          class="input w-full"
          :placeholder="$t('finances.expenses.modals.edit_expense.date_placeholder')"
          required
        />

        <label for="description" class="label">{{ $t('finances.expenses.modals.edit_expense.description') }}</label>
        <input
          type="text"
          v-model="expense.description"
          class="input w-full"
          :placeholder="$t('finances.expenses.modals.edit_expense.description_placeholder')"
          required
        />
      </div>
    </BaseDialog>
    <!-- Create Modal -->
    <BaseDialog
      v-model="createModal"
      @confirm="createExpense"
      :title="$t('finances.expenses.modals.create_expense.title')"
      :confirmText="$t('common.create')"
      :cancelText="$t('common.cancel')"
      @cancel="closeCreateModal"
    >
      <!-- Inputs: (amount, category, date, description) -->
      <div class="flex flex-col gap-2 w-full">
        <label for="amount" class="label">{{ $t('finances.expenses.modals.create_expense.amount') }}</label>
        <input
          type="number"
          v-model="expense.amount"
          class="input w-full"
          :placeholder="$t('finances.expenses.modals.create_expense.amount_placeholder')"
          required
        />

        <label for="category" class="label">{{ $t('finances.expenses.modals.create_expense.category') }}</label>
        <input
          type="text"
          v-model="expense.category"
          class="input w-full"
          :placeholder="$t('finances.expenses.modals.create_expense.category_placeholder')"
          required
        />

        <label for="date" class="label">{{ $t('finances.expenses.modals.create_expense.date') }}</label>
        <input
          type="date"
          v-model="expense.date"
          class="input w-full"
          :placeholder="$t('finances.expenses.modals.create_expense.date_placeholder')"
          required
        />

        <label for="description" class="label">{{ $t('finances.expenses.modals.create_expense.description') }}</label>
        <input
          type="text"
          v-model="expense.description"
          class="input w-full"
          :placeholder="$t('finances.expenses.modals.create_expense.description_placeholder')"
          required
        />
      </div>
    </BaseDialog>

    <LoadingScreen v-if="expenseStore.loading"></LoadingScreen>
  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useExpenseStore } from '@/stores/expense'
import { Chart } from 'chart.js/auto'
import LoadingScreen from '@/components/common/LoadingScreen.vue';

export default {
  components: { BaseDialog, LoadingScreen },
  data() {
    return {
      expenseStore: useExpenseStore(),
      categoryChartInstance: null,
      timelineChartInstance: null,

      // modals
      createModal: false,
      updateModal: false,
      deleteModal: false,

      // form object
      expense: {
        amount: null,
        category: '',
        date: '',
        description: '',
      },

      selectedExpense: null,
    }
  },

  async mounted() {
    await this.expenseStore.getExpenses()
    await this.expenseStore.getStats()

    this.updateCharts()
  },

  computed: {
    total() {
      return this.expenseStore.expenses.reduce((sum, e) => sum + e.amount, 0)
    },

    topCategory() {
      if (!this.expenseStore.stats.length) return null

      return this.expenseStore.stats.reduce((max, item) => (item.total > max.total ? item : max))
    },

    todayTotal() {
      const today = new Date().toISOString().slice(0, 10)

      return this.expenseStore.expenses
        .filter((e) => e.date.startsWith(today))
        .reduce((sum, e) => sum + e.amount, 0)
    },

    chartData() {
      return {
        labels: this.expenseStore.stats.map((s) => s.category),
        data: this.expenseStore.stats.map((s) => s.total),
      }
    },

    timelineData() {
      const grouped = {}

      this.expenseStore.expenses.forEach((e) => {
        const date = e.date.slice(0, 10)

        if (!grouped[date]) {
          grouped[date] = 0
        }

        grouped[date] += e.amount
      })

      return {
        labels: Object.keys(grouped),
        data: Object.values(grouped),
      }
    },
  },

  methods: {
    openDelete(expense) {
      this.selectedExpense = expense
      this.deleteModal = true
    },

    async deleteExpense() {
      await this.expenseStore.deleteExpense(this.selectedExpense.id)
      this.deleteModal = false

      await this.expenseStore.getExpenses()
      await this.expenseStore.getStats()
      this.updateCharts()
    },

    closeDelete() {
      this.deleteModal = false
    },
    openUpdate(expense) {
      this.selectedExpense = expense

      this.expense = {
        amount: expense.amount,
        category: expense.category,
        date: expense.date.slice(0, 10),
        description: expense.description,
      }

      this.updateModal = true
    },

    async updateExpense() {
      await this.expenseStore.updateExpense(
        this.selectedExpense.id || this.selectedExpense.expense_id,
        this.expense,
      )
      await this.expenseStore.getExpenses()
      await this.expenseStore.getStats()
      this.updateCharts()

      this.updateModal = false
    },

    closeUpdate() {
      this.updateModal = false
    },
    async openCreate() {
      this.expense = {
        amount: null,
        category: '',
        date: '',
        description: '',
      }

      this.createModal = true
    },

    async createExpense() {
      await this.expenseStore.createExpense(this.expense)
      this.createModal = false
      await this.expenseStore.getExpenses()
      await this.expenseStore.getStats()
      this.updateCharts()
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('lv-LV')
    },
    async nextPage() {
      await this.expenseStore.nextPage()
      await this.expenseStore.getExpenses()
      await this.expenseStore.getStats()
      this.updateCharts()
    },

    async prevPage() {
      await this.expenseStore.prevPage()
      await this.expenseStore.getExpenses()
      await this.expenseStore.getStats()
      this.updateCharts()
    },

    updateCharts() {
      this.$nextTick(() => {
        requestAnimationFrame(() => {
          this.renderCategoryChart()
          this.renderTimelineChart()
        })
      })
    },

    renderCategoryChart() {
      if (this.categoryChartInstance) {
        this.categoryChartInstance.destroy()
      }

      const ctx = this.$refs.categoryChart

      this.categoryChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.chartData.labels,
          datasets: [
            {
              label: this.$t('finances.expenses.category_charts'),
              data: this.chartData.data,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      })
    },

    renderTimelineChart() {
      if (this.timelineChartInstance) {
        this.timelineChartInstance.destroy()
      }

      const ctx = this.$refs.timelineChart

      this.timelineChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.timelineData.labels,
          datasets: [
            {
              label: this.$t('finances.expenses.daily_spending'),
              data: this.timelineData.data,
              borderColor: '#16a34a',
              backgroundColor: 'rgba(22,163,74,0.2)',
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      })
    },
  },
}
</script>
