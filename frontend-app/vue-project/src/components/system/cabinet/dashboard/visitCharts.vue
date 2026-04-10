<template>
    <!-- Visit charts -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">

        <!-- Bar Chart -->
        <div class="card bg-base-200 border border-base-300 rounded-none p-4">

            <h3 class="text-lg font-semibold mb-2">
                Avg Time per Visit (min)
            </h3>

            <!-- No data -->
            <div v-if="!hasData"
                class="alert bg-base-100 border border-base-300 flex flex-col gap-2 items-center justify-center h-55">
                <font-awesome-icon icon="fa-solid fa-chart-column"
                    class="text-3xl text-base-content/40 animate-bounce" />

                <span class="text-sm text-base-content/60 font-medium">
                    No visit data yet
                </span>

                <span class="text-xs text-base-content/40">
                    Your activity charts will appear here
                </span>
            </div>

            <!-- Chart -->
            <canvas v-else ref="barChart"></canvas>

        </div>


        <!-- Line Chart -->
        <div class="card bg-base-200 border border-base-300 rounded-none p-4">

            <h3 class="text-lg font-semibold mb-2">
                Total Time per Day (min)
            </h3>

            <!-- No data -->
            <div v-if="!hasData"
                class="alert bg-base-100 border border-base-300 flex flex-col gap-2 items-center justify-center h-55">
                <font-awesome-icon icon="fa-solid fa-chart-line" class="text-3xl text-base-content/40 animate-pulse" />

                <span class="text-sm text-base-content/60 font-medium">
                    No time statistics yet
                </span>

                <span class="text-xs text-base-content/40">
                    Start using the app to generate stats
                </span>
            </div>

            <!-- Chart -->
            <canvas v-else ref="lineChart"></canvas>

        </div>

    </div>
</template>

<script>
import { Chart, registerables } from 'chart.js'
import { useVisitsStore } from '@/stores/visits'

Chart.register(...registerables)

export default {

    name: 'VisitCharts',

    data() {
        return {
            visitsStore: useVisitsStore(),
            barChartInstance: null,
            lineChartInstance: null,
        }
    },

    computed: {
        hasData() {
            return (
                this.visitsStore.visits?.daily_breakdown &&
                this.visitsStore.visits.daily_breakdown.length > 0
            )
        }
    },

    mounted() {

        this.visitsStore.getWeekStats()
            .then(() => {

                if (this.hasData) {
                    this.renderBarChart()
                    this.renderLineChart()
                }

            })
            .catch(console.error)

    },

    methods: {
        formatMinutes(seconds) {
            return (seconds / 60).toFixed(1)
        },

        formatHuman(seconds) {

            const m = Math.floor(seconds / 60)
            const s = seconds % 60

            if (m === 0)
                return `${s}s`

            if (s === 0)
                return `${m}m`

            return `${m}m ${s}s`
        },

        renderBarChart() {

            const labels =
                this.visitsStore.visits.daily_breakdown.map(d => d.date)

            const data =
                this.visitsStore.visits.daily_breakdown.map(d =>
                    d.visits > 0 ?
                        this.formatMinutes(d.seconds / d.visits)
                        : 0
                )

            const ctx =
                this.$refs.barChart.getContext('2d')

            if (this.barChartInstance)
                this.barChartInstance.destroy()

            this.barChartInstance =
                new Chart(ctx, {

                    type: 'bar',

                    data: {
                        labels,

                        datasets: [
                            {
                                data,
                                backgroundColor:
                                    'rgba(59,130,246,0.5)',
                                borderColor:
                                    'rgba(59,130,246,1)',
                                borderWidth: 1
                            }
                        ]
                    },

                    options: {
                        responsive: true,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: (ctx) => {

                                        const day =
                                            this.visitsStore.visits.daily_breakdown[ctx.dataIndex]

                                        if (!day.visits)
                                            return "No visits"

                                        const avgSeconds =
                                            Math.round(day.seconds / day.visits)

                                        return this.formatHuman(avgSeconds)
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }

                })

        },

        renderLineChart() {

            const labels =
                this.visitsStore.visits.daily_breakdown.map(d => d.date)

            const data =
                this.visitsStore.visits.daily_breakdown.map(d =>
                    this.formatMinutes(d.seconds)
                )

            const ctx =
                this.$refs.lineChart.getContext('2d')

            if (this.lineChartInstance)
                this.lineChartInstance.destroy()

            this.lineChartInstance =
                new Chart(ctx, {

                    type: 'line',

                    data: {
                        labels,

                        datasets: [
                            {
                                data,
                                fill: true,
                                backgroundColor:
                                    'rgba(34,197,94,0.2)',
                                borderColor:
                                    'rgba(34,197,94,1)',
                                tension: 0.3
                            }
                        ]
                    },

                    options: {
                        responsive: true,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: (ctx) => {

                                        const seconds =
                                            this.visitsStore.visits.daily_breakdown[ctx.dataIndex].seconds

                                        return this.formatHuman(seconds)
                                    }
                                }
                            }
                        }
                    }

                })

        }

    }

}
</script>