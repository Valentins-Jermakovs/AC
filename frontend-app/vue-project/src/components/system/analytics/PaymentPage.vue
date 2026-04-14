<template>
  <div class="h-full bg-base-100 p-4 flex flex-col gap-4">
    <!-- CARDS -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="card rounded-none border border-base-300 bg-base-200 p-4">
        <div class="text-sm opacity-70">Total Amount</div>
        <div class="text-2xl font-bold">€{{ totalAmount }}</div>
      </div>

      <div class="card rounded-none border border-base-300 bg-base-200 p-4">
        <div class="text-sm opacity-70">Recurring Payments</div>
        <div class="text-2xl font-bold">{{ paymentStore.meta.total_items }}</div>
      </div>

      <div class="card rounded-none border border-base-300 bg-base-200 p-4">
        <div class="text-sm opacity-70">Next Payment</div>
        <div class="text-2xl font-bold">{{ nextPaymentLabel }}</div>
      </div>

      <div class="card rounded-none border border-base-300 bg-base-200 p-4">
        <div class="text-sm opacity-70">Average Amount</div>
        <div class="text-2xl font-bold">€{{ averageAmount }}</div>
      </div>
    </div>

    <!-- CHARTS -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 flex-1">
      <div class="card rounded-none border border-base-300 bg-base-200 p-4 h-80 flex flex-col">
        <div class="font-semibold mb-2">Amount by Category</div>
        <div class="flex-1 relative">
          <canvas ref="categoryChart"></canvas>
        </div>
      </div>

      <div class="card rounded-none border border-base-300 bg-base-200 p-4 h-80 flex flex-col">
        <div class="font-semibold mb-2">Upcoming Schedule</div>
        <div class="flex-1 relative">
          <canvas ref="timelineChart"></canvas>
        </div>
      </div>
    </div>

    <div class="flex justify-end">
      <button class="btn btn-primary btn-sm" @click="openCreate">+ New Payment</button>
    </div>

    <!-- TABLE -->
    <div class="card rounded-none border border-base-300 bg-base-200 p-4 flex flex-col gap-3">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div class="font-semibold">Recurring Payments</div>
        <div class="text-sm opacity-70">
          Page {{ paymentStore.meta.page }} / {{ paymentStore.meta.total_pages }}
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="table table-sm w-full">
          <thead>
            <tr>
              <th>Category</th>
              <th>Amount</th>
              <th>Start Date</th>
              <th>Interval</th>
              <th class="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="payment in payments" :key="payment.id">
              <td>
                <span class="badge badge-outline">{{ payment.category }}</span>
              </td>
              <td class="font-medium">€{{ payment.amount }}</td>
              <td>{{ formatDate(payment.start_date) }}</td>
              <td class="opacity-70">{{ payment.interval }}</td>
              <td class="text-right">
                <div class="flex justify-end gap-2">
                  <button class="btn btn-xs btn-info" @click="openUpdate(payment)">Edit</button>
                  <button class="btn btn-xs btn-error" @click="openDelete(payment)">Delete</button>
                </div>
              </td>
            </tr>
            <tr v-if="!payments.length">
              <td colspan="5" class="text-center opacity-60 py-6">No payments found</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex justify-between items-center pt-2">
        <button class="btn btn-sm" :disabled="paymentStore.meta.page <= 1" @click="prevPage">
          Prev
        </button>
        <div class="text-sm opacity-70">{{ paymentStore.meta.total_items }} total</div>
        <button
          class="btn btn-sm"
          :disabled="paymentStore.meta.page >= paymentStore.meta.total_pages"
          @click="nextPage"
        >
          Next
        </button>
      </div>
    </div>

    <BaseDialog
      v-model="deleteModal"
      title="Delete Payment"
      :confirmText="$t('common.delete')"
      :cancelText="$t('common.cancel')"
      @confirm="deletePayment"
      @cancel="closeDelete"
    >
      <p>Are you sure you want to delete this recurring payment?</p>
    </BaseDialog>

    <BaseDialog
      v-model="updateModal"
      title="Update Payment"
      :confirmText="$t('common.update')"
      :cancelText="$t('common.cancel')"
      @confirm="updatePayment"
      @cancel="closeUpdate"
    >
      <div class="flex flex-col gap-3">
        <input
          v-model.number="form.amount"
          type="number"
          class="input input-bordered w-full"
          placeholder="Amount"
        />
        <input v-model="form.category" class="input input-bordered w-full" placeholder="Category" />
        <input
          v-model="form.start_date"
          type="date"
          class="input input-bordered w-full"
          placeholder="Start Date"
        />
        <select v-model="form.interval" class="select select-bordered w-full">
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
      </div>
    </BaseDialog>

    <BaseDialog
      v-model="createModal"
      title="Create Payment"
      :confirmText="$t('common.create')"
      :cancelText="$t('common.cancel')"
      @confirm="createPayment"
      @cancel="closeCreate"
    >
      <div class="flex flex-col gap-3">
        <input
          v-model.number="form.amount"
          type="number"
          class="input input-bordered w-full"
          placeholder="Amount"
        />
        <input v-model="form.category" class="input input-bordered w-full" placeholder="Category" />
        <input
          v-model="form.start_date"
          type="date"
          class="input input-bordered w-full"
          placeholder="Start Date"
        />
        <select v-model="form.interval" class="select select-bordered w-full">
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
      </div>
    </BaseDialog>
  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { usePaymentStore } from '@/stores/payment'
import { Chart } from 'chart.js/auto'

export default {
  name: 'PaymentPage',
  components: { BaseDialog },
  data() {
    return {
      paymentStore: usePaymentStore(),
      categoryChartInstance: null,
      timelineChartInstance: null,
      createModal: false,
      updateModal: false,
      deleteModal: false,
      selectedPayment: null,
      form: {
        amount: null,
        category: '',
        start_date: '',
        interval: 'monthly',
      },
    }
  },
  async mounted() {
    await this.paymentStore.fetchPayments()
    this.updateCharts()
  },
  computed: {
    payments() {
      return this.paymentStore?.payments || []
    },
    totalAmount() {
      return Number(this.payments.reduce((sum, payment) => sum + payment.amount, 0)).toFixed(2)
    },
    averageAmount() {
      if (!this.payments.length) return '0.00'
      return (this.totalAmount / this.payments.length).toFixed(2)
    },
    nextPayment() {
      if (!this.payments.length) return null
      return [...this.payments].sort((a, b) => new Date(a.start_date) - new Date(b.start_date))[0]
    },
    nextPaymentLabel() {
      return this.nextPayment
        ? `${this.formatDate(this.nextPayment.start_date)} (${this.nextPayment.interval})`
        : '-'
    },
    categoryChartData() {
      const grouped = {}
      this.payments.forEach((payment) => {
        grouped[payment.category] = (grouped[payment.category] || 0) + payment.amount
      })
      return {
        labels: Object.keys(grouped),
        data: Object.values(grouped),
      }
    },
    timelineChartData() {
      const grouped = {}
      this.payments.forEach((payment) => {
        const date = payment.start_date
        grouped[date] = (grouped[date] || 0) + payment.amount
      })
      const sortedDates = Object.keys(grouped).sort((a, b) => new Date(a) - new Date(b))
      return {
        labels: sortedDates,
        data: sortedDates.map((date) => grouped[date]),
      }
    },
  },
  methods: {
    openCreate() {
      this.selectedPayment = null
      this.form = {
        amount: null,
        category: '',
        start_date: '',
        interval: 'monthly',
      }
      this.createModal = true
    },
    async createPayment() {
      await this.paymentStore.createPayment(this.form)
      this.createModal = false
      this.updateCharts()
    },
    openUpdate(payment) {
      this.selectedPayment = payment
      this.form = {
        amount: payment.amount,
        category: payment.category,
        start_date: payment.start_date,
        interval: payment.interval,
      }
      this.updateModal = true
    },
    async updatePayment() {
      if (!this.selectedPayment) return
      await this.paymentStore.updatePayment(this.form, this.selectedPayment.id)
      this.updateModal = false
      this.updateCharts()
    },
    openDelete(payment) {
      this.selectedPayment = payment
      this.deleteModal = true
    },
    async deletePayment() {
      if (!this.selectedPayment) return
      await this.paymentStore.deletePayment(this.selectedPayment.id)
      this.deleteModal = false
      this.updateCharts()
    },
    closeCreate() {
      this.createModal = false
    },
    closeUpdate() {
      this.updateModal = false
    },
    closeDelete() {
      this.deleteModal = false
    },
    async nextPage() {
      await this.paymentStore.nextPage()
      this.updateCharts()
    },
    async prevPage() {
      await this.paymentStore.prevPage()
      this.updateCharts()
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('lv-LV')
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
      if (!ctx) return
      this.categoryChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.categoryChartData.labels,
          datasets: [
            {
              label: 'Category Amount',
              data: this.categoryChartData.data,
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
      if (!ctx) return
      this.timelineChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.timelineChartData.labels,
          datasets: [
            {
              label: 'Upcoming Amount',
              data: this.timelineChartData.data,
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

<style scoped></style>
