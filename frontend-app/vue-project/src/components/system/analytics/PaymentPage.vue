<template>
  <div class="h-full bg-base-100 p-4 flex flex-col gap-4">
    <!-- CARDS -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="card rounded-none border border-base-300 bg-base-200 p-4">
        <div class="text-sm opacity-70">{{ $t('finances.payments.total_amount') }}</div>
        <div class="text-2xl font-bold">€{{ totalAmount }}</div>
      </div>

      <div class="card rounded-none border border-base-300 bg-base-200 p-4">
        <div class="text-sm opacity-70">{{ $t('finances.payments.recurring_payments') }}</div>
        <div class="text-2xl font-bold">{{ paymentStore.meta.total_items }}</div>
      </div>

      <div class="card rounded-none border border-base-300 bg-base-200 p-4">
        <div class="text-sm opacity-70">{{ $t('finances.payments.next_payment') }}</div>
        <div class="text-2xl font-bold" v-if="nextPaymentLabel !== '-'">{{ nextPaymentLabel }}</div>
        <div class="text-2xl font-bold text-base-content/70" v-else>
          <font-awesome-icon icon="fa-solid fa-spinner" class="text-2xl animate-spin" />
        </div>
      </div>

      <div class="card rounded-none border border-base-300 bg-base-200 p-4">
        <div class="text-sm opacity-70">{{ $t('finances.payments.average_payment') }}</div>
        <div class="text-2xl font-bold">€{{ averageAmount }}</div>
      </div>
    </div>

    <!-- CHARTS -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 flex-1">
      <div class="card rounded-none border border-base-300 bg-base-200 p-4 h-80 flex flex-col">
        <div class="font-semibold mb-2">{{ $t('finances.payments.amount_by_category') }}</div>
        <div class="flex-1 relative" v-if="paymentStore.payments.length > 0">
          <canvas ref="categoryChart"></canvas>
        </div>
        <div v-else class="flex flex-col items-center justify-center gap-2 h-full text-base-content/70">
          <font-awesome-icon icon="fa-solid fa-chart-line" class="text-4xl animate-bounce" />
          <p class="text-lg">{{ $t('finances.payments.no_payments') }}</p>
        </div>
      </div>

      <div class="card rounded-none border border-base-300 bg-base-200 p-4 h-80 flex flex-col">
        <div class="font-semibold mb-2">{{ $t('finances.payments.upcoming_schedule') }}</div>
        <div class="flex-1 relative" v-if="paymentStore.payments.length > 0">
          <canvas ref="timelineChart"></canvas>
        </div>
        <div v-else class="flex flex-col items-center justify-center gap-2 h-full text-base-content/70">
          <font-awesome-icon icon="fa-solid fa-chart-line" class="text-4xl animate-bounce" />
          <p class="text-lg">{{ $t('finances.payments.no_payments') }}</p>
        </div>
      </div>
    </div>

    <div class="flex justify-end">
      <button class="btn btn-primary btn-sm" @click="openCreate">
        <font-awesome-icon icon="fa-solid fa-pencil"></font-awesome-icon>
        {{ $t('finances.payments.new_payment') }}
      </button>
    </div>

    <!-- TABLE -->
    <div class="card rounded-none hidden md:flex border border-base-300 bg-base-200 p-4 flex-col gap-3">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div class="font-semibold">{{ $t('finances.payments.recurring_payments') }}</div>
        <div class="text-sm opacity-70">
          {{ $t('finances.payments.table.page') }} {{ paymentStore.meta.page }} / {{ paymentStore.meta.total_pages }}
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="table table-sm w-full">
          <thead>
            <tr>
              <th>{{ $t('finances.payments.table.category') }}</th>
              <th>{{ $t('finances.payments.table.amount') }}</th>
              <th>{{ $t('finances.payments.table.start_date') }}</th>
              <th>{{ $t('finances.payments.table.interval') }}</th>
              <th class="text-right">{{ $t('finances.payments.table.actions') }}</th>
            </tr>
          </thead>
          <tbody class="bg-base-100">
            <tr v-for="payment in payments" :key="payment.id">
              <td>
                <span class="badge badge-neutral">{{ payment.category }}</span>
              </td>
              <td class="font-medium">€{{ payment.amount }}</td>
              <td>{{ formatDate(payment.start_date) }}</td>
              <td class="opacity-70">
                <p v-if="payment.interval === 'daily'">{{ $t('finances.payments.daily_payments') }}</p>
                <p v-if="payment.interval === 'weekly'">{{ $t('finances.payments.weekly_payments') }}</p>
                <p v-if="payment.interval === 'monthly'">{{ $t('finances.payments.monthly_payments') }}</p>
              </td>
              <td class="text-right">
                <div class="flex justify-end gap-2">
                  <button class="btn btn-xs btn-info" @click="openUpdate(payment)">{{ $t('finances.payments.table.edit')
                  }}</button>
                  <button class="btn btn-xs btn-error" @click="openDelete(payment)">{{
                    $t('finances.payments.table.delete') }}</button>
                </div>
              </td>
            </tr>
            <tr v-if="!payments.length">
              <td colspan="5" class="text-center opacity-60 py-6">
                <font-awesome-icon icon="fa-solid fa-wallet" class="text-2xl animate-bounce" />
                <p class="text-error animate-bounce">{{ $t('finances.payments.no_payments') }}</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex justify-between items-center pt-2">
        <button class="btn btn-sm btn-neutral" :disabled="paymentStore.meta.page <= 1" @click="prevPage">
          {{ $t('finances.payments.table.prev') }}
        </button>
        <div class="text-sm opacity-70">{{ $t('finances.payments.table.total') }} {{ paymentStore.meta.total_items }}
        </div>
        <button class="btn btn-sm btn-neutral" :disabled="paymentStore.meta.page >= paymentStore.meta.total_pages"
          @click="nextPage">
          {{ $t('finances.payments.table.next') }}
        </button>
      </div>
    </div>

    <!-- MOBILE -->
    <div class="card rounded-none md:hidden border border-base-300 bg-base-200 p-4 flex flex-col gap-3">

      <!-- HEADER -->
      <div class="flex justify-between items-center">
        <div class="font-semibold">
          {{ $t('finances.payments.recurring_payments') }}
        </div>

        <div class="text-xs opacity-70 text-right">
          {{ paymentStore.meta.page }} / {{ paymentStore.meta.total_pages }}
        </div>
      </div>

      <!-- LIST -->
      <div class="flex flex-col gap-3">

        <div v-for="payment in payments" :key="payment.id" class="card rounded-none bg-base-100 border border-base-300 p-3">
          <!-- TOP -->
          <div class="flex justify-between items-center">
            <span class="badge badge-neutral">
              {{ payment.category }}
            </span>

            <span class="font-semibold">
              €{{ payment.amount }}
            </span>
          </div>

          <!-- INFO -->
          <div class="mt-2 text-sm opacity-70 flex justify-between">
            <span>{{ formatDate(payment.start_date) }}</span>

            <span>
              <span v-if="payment.interval === 'daily'">
                {{ $t('finances.payments.daily_payments') }}
              </span>
              <span v-if="payment.interval === 'weekly'">
                {{ $t('finances.payments.weekly_payments') }}
              </span>
              <span v-if="payment.interval === 'monthly'">
                {{ $t('finances.payments.monthly_payments') }}
              </span>
            </span>
          </div>

          <!-- ACTIONS -->
          <div class="flex gap-2 mt-3">
            <button class="btn btn-xs btn-info flex-1" @click="openUpdate(payment)">
              {{ $t('finances.payments.table.edit') }}
            </button>

            <button class="btn btn-xs btn-error flex-1" @click="openDelete(payment)">
              {{ $t('finances.payments.table.delete') }}
            </button>
          </div>
        </div>

        <!-- EMPTY -->
        <div v-if="!payments.length" class="text-center opacity-60 py-6">
          <font-awesome-icon icon="fa-solid fa-wallet" class="text-2xl animate-bounce" />
          <p class="text-error animate-bounce">{{ $t('finances.payments.no_payments') }}</p>
        </div>
      </div>

      <!-- PAGINATION -->
      <div class="flex justify-between items-center pt-2">
        <button class="btn btn-sm btn-neutral" :disabled="paymentStore.meta.page <= 1" @click="prevPage">
          {{ $t('finances.payments.table.prev') }}
        </button>

        <div class="text-sm opacity-70 text-center">
          {{ $t('finances.payments.table.total') }}
          {{ paymentStore.meta.total_items }}
        </div>

        <button class="btn btn-sm btn-neutral" :disabled="paymentStore.meta.page >= paymentStore.meta.total_pages"
          @click="nextPage">
          {{ $t('finances.payments.table.next') }}
        </button>
      </div>
    </div>

    <BaseDialog v-model="deleteModal" :title="$t('finances.payments.modals.delete_payment.title')"
      :confirmText="$t('common.delete')" :cancelText="$t('common.cancel')" @confirm="deletePayment"
      @cancel="closeDelete">
      <Transition name="error-slide">
        <div v-if="error" class="mb-4">
          <div class="alert alert-error">
            <span>{{ error }}</span>
          </div>
        </div>
      </Transition>
      <p>{{ $t('finances.payments.modals.delete_payment.content') }}</p>
    </BaseDialog>

    <BaseDialog v-model="updateModal" :title="$t('finances.payments.modals.edit_payment.title')"
      :confirmText="$t('common.confirm')" :cancelText="$t('common.cancel')" @confirm="updatePayment"
      @cancel="closeUpdate">
      
      <div class="flex flex-col gap-2 w-full">
        <Transition name="error-slide">
        <div v-if="error" class="mb-4">
          <div class="text-error">
            <span>{{ error }}</span>
          </div>
        </div>
      </Transition>
        <label for="amount" class="label">{{ $t('finances.payments.modals.edit_payment.amount') }}</label>
        <input v-model.number="form.amount" type="number" class="input input-bordered w-full"
          :placeholder="$t('finances.payments.modals.edit_payment.amount_placeholder')" />
        <label for="category" class="label">{{ $t('finances.payments.modals.edit_payment.category') }}</label>
        <input v-model="form.category" class="input input-bordered w-full"
          :placeholder="$t('finances.payments.modals.edit_payment.category_placeholder')" />
        <label for="start_date" class="label">{{ $t('finances.payments.modals.edit_payment.start_date') }}</label>
        <input v-model="form.start_date" type="date" class="input input-bordered w-full"
          :placeholder="$t('finances.payments.modals.edit_payment.start_date_placeholder')" />
        <label for="interval" class="label">{{ $t('finances.payments.modals.edit_payment.interval') }}</label>
        <select v-model="form.interval" class="select select-bordered w-full">
          <option value="daily">{{ $t('finances.payments.daily_payments') }}</option>
          <option value="weekly">{{ $t('finances.payments.weekly_payments') }}</option>
          <option value="monthly">{{ $t('finances.payments.monthly_payments') }}</option>
        </select>
      </div>
    </BaseDialog>

    <BaseDialog v-model="createModal" :title="$t('finances.payments.modals.create_payment.title')"
      :confirmText="$t('common.create')" :cancelText="$t('common.cancel')" @confirm="createPayment"
      @cancel="closeCreate">
      
      <div class="flex flex-col gap-2 w-full">
        <Transition name="error-slide">
        <div v-if="error" class="mb-4">
          <div class="text-error">
            <span>{{ error }}</span>
          </div>
        </div>
      </Transition>
        <label for="amount" class="label">{{ $t('finances.payments.modals.create_payment.amount') }}</label>
        <input v-model.number="form.amount" type="number" class="input input-bordered w-full"
          :placeholder="$t('finances.payments.modals.create_payment.amount_placeholder')" />
        <label for="category" class="label">{{ $t('finances.payments.modals.create_payment.category') }}</label>
        <input v-model="form.category" class="input input-bordered w-full"
          :placeholder="$t('finances.payments.modals.create_payment.category_placeholder')" />
        <label for="start_date" class="label">{{ $t('finances.payments.modals.create_payment.start_date') }}</label>
        <input v-model="form.start_date" type="date" class="input input-bordered w-full"
          :placeholder="$t('finances.payments.modals.create_payment.start_date_placeholder')" />
        <label for="interval" class="label">{{ $t('finances.payments.modals.create_payment.interval') }}</label>
        <select v-model="form.interval" class="select select-bordered w-full">
          <option value="daily">{{ $t('finances.payments.daily_payments') }}</option>
          <option value="weekly">{{ $t('finances.payments.weekly_payments') }}</option>
          <option value="monthly">{{ $t('finances.payments.monthly_payments') }}</option>
        </select>
      </div>
    </BaseDialog>

    <LoadingScreen v-if="paymentStore.loading"></LoadingScreen>
  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import LoadingScreen from '@/components/common/LoadingScreen.vue';
import { usePaymentStore } from '@/stores/payment'
import { Chart } from 'chart.js/auto'

export default {
  name: 'PaymentPage',
  components: { BaseDialog, LoadingScreen },
  data() {
    return {
      paymentStore: usePaymentStore(),
      categoryChartInstance: null,
      timelineChartInstance: null,
      createModal: false,
      updateModal: false,
      deleteModal: false,
      selectedPayment: null,
      error: null,
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
      if (!this.nextPayment) return '-'

      const intervalMap = {
        daily: this.$t('finances.payments.daily_payments'),
        weekly: this.$t('finances.payments.weekly_payments'),
        monthly: this.$t('finances.payments.monthly_payments')
      }

      const intervalLabel = intervalMap[this.nextPayment.interval] || this.nextPayment.interval

      return `${this.formatDate(this.nextPayment.start_date)} (${intervalLabel})`
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
      this.error = null
      this.form = {
        amount: null,
        category: '',
        start_date: '',
        interval: 'monthly',
      }
      this.createModal = true
    },

    async createPayment() {
      try {
        this.error = null
        await this.paymentStore.createPayment(this.form)

        if (this.paymentStore.error) {
          this.error = this.paymentStore.error
          return
        }

        this.createModal = false
        this.updateCharts()
      } catch (err) {
        this.error = this.paymentStore.error || err.message || 'Failed to create payment'
        console.error('Error creating payment:', err)
      }
    },

    closeCreate() {
      this.createModal = false
      this.error = null
    },

    openUpdate(payment) {
      this.selectedPayment = payment
      this.error = null
      this.form = {
        amount: payment.amount,
        category: payment.category,
        start_date: payment.start_date,
        interval: payment.interval,
      }
      this.updateModal = true
    },

    async updatePayment() {
      try {
        this.error = null
        if (!this.selectedPayment) return
        await this.paymentStore.updatePayment(this.form, this.selectedPayment.id)

        if (this.paymentStore.error) {
          this.error = this.paymentStore.error
          return
        }

        this.updateModal = false
        this.updateCharts()
      } catch (err) {
        this.error = this.paymentStore.error || err.message || 'Failed to update payment'
        console.error('Error updating payment:', err)
      }
    },

    closeUpdate() {
      this.updateModal = false
      this.error = null
    },

    openDelete(payment) {
      this.selectedPayment = payment
      this.error = null
      this.deleteModal = true
    },

    async deletePayment() {
      try {
        this.error = null
        if (!this.selectedPayment) return
        await this.paymentStore.deletePayment(this.selectedPayment.id)

        if (this.paymentStore.error) {
          this.error = this.paymentStore.error
          return
        }

        this.deleteModal = false
        this.updateCharts()
      } catch (err) {
        this.error = this.paymentStore.error || err.message || 'Failed to delete payment'
        console.error('Error deleting payment:', err)
      }
    },

    closeDelete() {
      this.deleteModal = false
      this.error = null
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
              label: this.$t('finances.payments.category_amount'),
              data: this.categoryChartData.data,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.95)',
              titleColor: '#ffffff',
              bodyColor: '#ffffff',
              padding: 12,
              displayColors: false,
              font: {
                size: 13,
                weight: '500',
              },
            },
          },
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
              label: this.$t('finances.payments.upcoming_amount'),
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
          plugins: {
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.95)',
              titleColor: '#ffffff',
              bodyColor: '#ffffff',
              padding: 12,
              displayColors: false,
              font: {
                size: 13,
                weight: '500',
              },
            },
          },
        },
      })
    },
  },
}
</script>

<style scoped></style>
