<template>
  <div class="h-full bg-base-100 p-6 flex flex-col gap-6">

    <!-- HEADER -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-xl font-bold">Budgets</h1>
        <p class="text-sm opacity-60">
          {{ budgetStore.yearAndMonth }}
        </p>
      </div>

      <button class="btn btn-primary btn-sm" @click="openCreate">
        + New Budget
      </button>
    </div>

    <!-- STATS -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">

      <div class="card rounded-none bg-base-200 border border-base-300 p-4">
        <div class="text-sm opacity-60">Total Budgets</div>
        <div class="text-2xl font-bold">{{ budgets.length }}</div>
      </div>

      <div class="card rounded-none bg-base-200 border border-base-300 p-4">
        <div class="text-sm opacity-60">Total Limit</div>
        <div class="text-2xl font-bold">€{{ totalLimit }}</div>
      </div>

      <div class="card rounded-none bg-base-200 border border-base-300 p-4">
        <div class="text-sm opacity-60">Month</div>
        <div class="text-2xl font-bold">{{ budgetStore.yearAndMonth }}</div>
      </div>

    </div>

    <!-- CHART -->
    <div class="card rounded-none bg-base-200 border border-base-300 p-4 h-80 flex flex-col">
      <div class="font-semibold mb-2">Budget Limits</div>
      <div class="flex-1">
        <canvas ref="budgetChart"></canvas>
      </div>
    </div>

    <!-- TABLE -->
    <div class="card rounded-none bg-base-200 border border-base-300 p-4">

      <div class="font-semibold mb-3">Budgets</div>

      <div class="overflow-x-auto">
        <table class="table table-sm w-full">

          <thead>
            <tr class="opacity-70">
              <th>Category</th>
              <th>Limit</th>
              <th>Month</th>
              <th class="text-right">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="b in budgets" :key="b.id">

              <td>
                <span class="badge badge-outline">
                  {{ b.category }}
                </span>
              </td>

              <td class="font-medium">
                €{{ b.planned_amount }}
              </td>

              <td class="opacity-70">
                {{ b.month }}
              </td>

              <td class="text-right">
                <div class="flex justify-end gap-2">
                  <button class="btn btn-xs btn-info" @click="openUpdate(b)">
                    Edit
                  </button>
                  <button class="btn btn-xs btn-error" @click="openDelete(b)">
                    Delete
                  </button>
                </div>
              </td>

            </tr>

            <tr v-if="!budgets.length">
              <td colspan="4" class="text-center opacity-60 py-6">
                No budgets found
              </td>
            </tr>
          </tbody>

        </table>
      </div>

    </div>

    <!-- CREATE / UPDATE MODAL -->
    <BaseDialog
      v-model="modal"
      :title="editing ? 'Update Budget' : 'Create Budget'"
      :confirmText="editing ? 'Update' : 'Create'"
      :cancelText="$t('common.cancel')"
      @confirm="saveBudget"
      @cancel="modal = false"
    >
      <div class="flex flex-col gap-3">
        <input
          v-model="form.category"
          class="input input-bordered w-full"
          placeholder="Category"
        />

        <input
          v-model.number="form.planned_amount"
          type="number"
          class="input input-bordered w-full"
          placeholder="Limit"
        />

        <input
          v-model="form.month"
          class="input input-bordered w-full"
          placeholder="YYYY-MM"
        />
      </div>
    </BaseDialog>

    <!-- DELETE -->
    <BaseDialog
      v-model="deleteModal"
      title="Delete Budget"
      :confirmText="$t('common.delete')"
      :cancelText="$t('common.cancel')"
      @confirm="deleteBudget"
      @cancel="deleteModal = false"
    >
      <p>Are you sure?</p>
    </BaseDialog>

  </div>
</template>

<script>
import { useBudgetStore } from '@/stores/budget'
import { Chart } from 'chart.js/auto'
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  components: { BaseDialog },

  data() {
    return {
      budgetStore: useBudgetStore(),

      modal: false,
      deleteModal: false,
      editing: false,
      selected: null,

      form: {
        category: '',
        planned_amount: 0,
        month: ''
      },

      chartInstance: null
    }
  },

  async mounted() {
    await this.budgetStore.fetchBudgets()
    this.renderChart()
  },

  computed: {
    budgets() {
      return this.budgetStore.budgets
    },

    totalLimit() {
      return this.budgets.reduce((s, b) => s + b.planned_amount, 0)
    }
  },

  methods: {

    async refresh() {
      await this.budgetStore.fetchBudgets()
      this.updateChart()
    },

    openCreate() {
      this.editing = false
      this.form = { category: '', planned_amount: 0, month: '' }
      this.modal = true
    },

    openUpdate(b) {
      this.editing = true
      this.selected = b
      this.form = {
        category: b.category,
        planned_amount: b.planned_amount,
        month: b.month
      }
      this.modal = true
    },

    async saveBudget() {
      const payload = {
        category: this.form.category,
        month: this.form.month,
        planned_amount: this.form.planned_amount
      }

      if (this.editing) {
        await this.budgetStore.updateBudget(this.selected.id, payload)
      } else {
        await this.budgetStore.createBudget(payload)
      }

      this.modal = false
      await this.refresh()
    },

    openDelete(b) {
      this.selected = b
      this.deleteModal = true
    },

    async deleteBudget() {
      await this.budgetStore.deleteBudget(this.selected.id)
      this.deleteModal = false
      await this.refresh()
    },

    renderChart() {
      if (this.chartInstance) this.chartInstance.destroy()

      const ctx = this.$refs.budgetChart.getContext('2d')

      this.chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.budgets.map(b => b.category),
          datasets: [
            {
              label: 'Limit',
              data: this.budgets.map(b => b.planned_amount)
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      })
    },

    updateChart() {
      this.$nextTick(() => this.renderChart())
    }
  }
}
</script>