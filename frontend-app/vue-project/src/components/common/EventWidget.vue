<template>

    <!-- EVENT EXISTS -->
    <div v-if="closestEvent" class="w-full bg-base-200 border border-base-300 flex flex-col">

        <!-- HEADER -->
        <div class="w-full h-56 bg-base-10000 relative">

            <img src="@/assets/images/aaron-burden-n3OZeX6bR0g-unsplash.jpg" class="w-full h-full object-cover" />

            <div class="absolute inset-0 bg-black/50 flex flex-col justify-end p-5 gap-2">

                <h1 class="text-3xl font-bold text-white flex items-center gap-3">
                    <font-awesome-icon icon="fa-solid fa-calendar" />
                    {{ closestEvent.title }}
                </h1>

                <div class="flex gap-2">

                    <span :class="`badge badge-${closestEvent.color}`">
                        <font-awesome-icon icon="fa-solid fa-palette" class="mr-1" />
                        {{ closestEvent.color }}
                    </span>

                    <span class="badge badge-info">
                        <font-awesome-icon icon="fa-solid fa-circle-info" class="mr-1" />
                        {{ closestEvent.status }}
                    </span>

                </div>

            </div>

        </div>


        <!-- BODY -->
        <div class="p-5 flex flex-col gap-5">

            <!-- DESCRIPTION -->
            <div class="flex gap-3 bg-base-100 border border-base-300 p-4">

                <font-awesome-icon icon="fa-solid fa-align-left" class="text-xl text-primary mt-1" />

                <div class="flex flex-col gap-1">

                    <span class="text-sm text-base-content/60">
                        Description
                    </span>

                    <p class="text-base-content/80">
                        {{ closestEvent.description }}
                    </p>

                </div>

            </div>


            <!-- DATE INFO -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

                <!-- START -->
                <div class="flex gap-3 bg-base-100 border border-base-300 p-4">

                    <font-awesome-icon icon="fa-solid fa-calendar-plus" class="text-success text-xl mt-1" />

                    <div class="flex flex-col">

                        <span class="text-sm text-base-content/60">
                            Start
                        </span>

                        <span class="font-semibold">
                            {{ closestEvent.startDate }}
                        </span>

                        <span class="text-sm text-base-content/70">
                            {{ closestEvent.startTime }}
                        </span>

                    </div>

                </div>


                <!-- END -->
                <div class="flex gap-3 bg-base-100 border border-base-300 p-4">

                    <font-awesome-icon icon="fa-solid fa-calendar-check" class="text-error text-xl mt-1" />

                    <div class="flex flex-col">

                        <span class="text-sm text-base-content/60">
                            End
                        </span>

                        <span class="font-semibold">
                            {{ closestEvent.endDate }}
                        </span>

                        <span class="text-sm text-base-content/70">
                            {{ closestEvent.endTime }}
                        </span>

                    </div>

                </div>

            </div>


            <!-- EXTRA -->
            <div class="flex gap-3 bg-base-100 border border-base-300 p-4">

                <font-awesome-icon icon="fa-solid fa-clock" class="text-warning text-xl" />

                <div class="flex flex-col">

                    <span class="text-sm text-base-content/60">
                        Duration
                    </span>

                    <span class="font-semibold">
                        {{ closestEvent.allDay ? "All day event" : "Timed event" }}
                    </span>

                </div>

            </div>

        </div>

    </div>


    <!-- NO EVENTS IN MONTH -->
    <div v-else
        class="w-full bg-base-200 border border-base-300 p-10 flex flex-col items-center justify-center gap-4 text-center">

        <font-awesome-icon icon="fa-solid fa-calendar-xmark" class="text-5xl text-base-content/40" />

        <div class="flex flex-col gap-1">

            <h2 class="text-xl font-semibold">
                No events this month
            </h2>

            <p class="text-base-content/60">
                Nothing is planned for this month yet.
            </p>

        </div>

    </div>

</template>

<script>
import { useEventsStore } from '@/stores/events';

export default {
    name: 'EventWidget',

    data() {
        return {
            eventsStore: useEventsStore(),
        }
    },

    computed: {
        closestEvent() {
            if (!this.eventsStore.events.length) return null

            return [...this.eventsStore.events].sort(
                (a, b) => new Date(a.startDate) - new Date(b.startDate)
            )[0]
        }
    },

    async mounted() {
        const now = new Date()
        await this.eventsStore.getEventsByMonth(now.getMonth() + 1, now.getFullYear())
    }
}

</script>

<style scoped></style>