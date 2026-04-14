<template>
    <div class="h-full bg-base-100 p-4 flex flex-col gap-4">

        <!-- 🔲 CARDS -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

            <div class="card rounded-none border border-base-300 bg-base-200 p-4">
                <div class="text-sm opacity-70">Total Spent</div>
                <div class="text-2xl font-bold">€{{ total }}</div>
            </div>

            <div class="card rounded-none border border-base-300 bg-base-200 p-4">
                <div class="text-sm opacity-70">Transactions</div>
                <div class="text-2xl font-bold">
                    {{ expenseStore.meta.total_expenses }}
                </div>
            </div>

            <div class="card  rounded-none border border-base-300 bg-base-200 p-4">
                <div class="text-sm opacity-70">Top Category</div>
                <div class="text-2xl font-bold">
                    {{ topCategory?.category || '-' }}
                </div>
            </div>

            <div class="card rounded-none border border-base-300 bg-base-200 p-4">
                <div class="text-sm opacity-70">Today</div>
                <div class="text-2xl font-bold">€{{ todayTotal }}</div>
            </div>

        </div>

        <!-- 📊 CHARTS -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 flex-1">

            <div class="card rounded-none border border-base-300 bg-base-200 p-4 h-80 flex flex-col">
                <div class="font-semibold mb-2">Category Chart</div>

                <div class="flex-1 relative">
                    <canvas ref="categoryChart"></canvas>
                </div>
            </div>

            <div class="card rounded-none border border-base-300 bg-base-200 p-4 h-80 flex flex-col">
                <div class="font-semibold mb-2">Timeline</div>

                <div class="flex-1 relative">
                    <canvas ref="timelineChart"></canvas>
                </div>
            </div>

        </div>

    </div>
</template>

<script>
import { useExpenseStore } from '@/stores/expense'
import { Chart } from 'chart.js/auto'

export default {
    data() {
        return {
            expenseStore: useExpenseStore(),
            categoryChartInstance: null,
            timelineChartInstance: null
        }
    },

    async mounted() {
        await this.expenseStore.getExpenses()
        await this.expenseStore.getStats()

        this.$nextTick(() => {
            this.renderCategoryChart()
            this.renderTimelineChart()
        })
    },

    computed: {

        total() {
            return this.expenseStore.expenses.reduce(
                (sum, e) => sum + e.amount,
                0
            )
        },

        topCategory() {
            if (!this.expenseStore.stats.length) return null

            return this.expenseStore.stats.reduce((max, item) =>
                item.total > max.total ? item : max
            )
        },

        todayTotal() {
            const today = new Date().toISOString().slice(0, 10)

            return this.expenseStore.expenses
                .filter(e => e.date.startsWith(today))
                .reduce((sum, e) => sum + e.amount, 0)
        },

        chartData() {
            return {
                labels: this.expenseStore.stats.map(s => s.category),
                data: this.expenseStore.stats.map(s => s.total)
            }
        },

        timelineData() {
            const grouped = {}

            this.expenseStore.expenses.forEach(e => {
                const date = e.date.slice(0, 10)

                if (!grouped[date]) {
                    grouped[date] = 0
                }

                grouped[date] += e.amount
            })

            return {
                labels: Object.keys(grouped),
                data: Object.values(grouped)
            }
        }
    },

    methods: {

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
                            label: 'Expenses by Category',
                            data: this.chartData.data
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
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
                            label: 'Daily Spending',
                            data: this.timelineData.data
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            })
        }
    }
}
</script>