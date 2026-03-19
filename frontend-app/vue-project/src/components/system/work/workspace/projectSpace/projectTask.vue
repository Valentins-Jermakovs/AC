<template>
    <div class="drawer drawer-end">

        <input id="task-info-drawer" type="checkbox" class="drawer-toggle" />

        <!-- CONTENT -->
        <div class="drawer-content">

            <div class="w-full bg-base-100 border border-base-300
        rounded-box p-3 flex items-center justify-between">

                <!-- LEFT -->
                <div class="flex gap-2 flex-1">
                    <div class="flex items-center gap-3">
                        <h3 class="font-medium">Task title</h3>
                        <div class="badge badge-primary badge-outline">ToDo</div>
                    </div>

                    <!-- META BADGES -->
                    <div class="flex flex-wrap gap-2 text-xs">
                        <div class="badge badge-neutral gap-2">
                            <font-awesome-icon icon="fa-solid fa-layer-group" />
                            SP: 3
                        </div>
                        <div class="badge badge-secondary gap-2">
                            <font-awesome-icon icon="fa-solid fa-flag" />
                            Priority: 1
                        </div>
                        <div class="badge badge-neutral gap-2">
                            <font-awesome-icon icon="fa-solid fa-calendar" />
                            2026-12-31
                        </div>
                        <div class="badge badge-warning gap-2">
                            <font-awesome-icon icon="fa-solid fa-clock" />
                            2026-12-31
                        </div>
                    </div>
                </div>

                <!-- RIGHT: OPEN DRAWER BUTTON -->
                <label for="task-info-drawer" class="btn btn-primary btn-sm gap-2">
                    <font-awesome-icon icon="fa-solid fa-bars" />
                </label>

            </div>
        </div>
        <!-- DRAWER -->
        <div class="drawer-side">

            <label for="task-info-drawer" class="drawer-overlay"></label>

            <div class="bg-base-200 min-h-full w-96 p-6
            flex flex-col gap-6">

                <!-- HEADER -->
                <div class="flex justify-between items-center">
                    <h2 class="text-xl font-semibold">Task info</h2>
                    <button class="btn btn-ghost btn-sm btn-circle">✕</button>
                </div>

                <!-- CRUD ACTIONS -->
                <div class="bg-base-100 border border-base-300 rounded-box">
                    <ul class="menu w-full">
                        <li>
                            <button class="flex gap-3">
                                <font-awesome-icon icon="fa-solid fa-plus" />
                                Create task
                            </button>
                        </li>
                        <li>
                            <button class="flex gap-3">
                                <font-awesome-icon icon="fa-solid fa-pen" />
                                Update task
                            </button>
                        </li>
                        <li class="border-t border-base-300 mt-2 pt-2">
                            <button class="text-error flex gap-3">
                                <font-awesome-icon icon="fa-solid fa-trash" />
                                Delete task
                            </button>
                        </li>
                    </ul>
                </div>

                <!-- DETAILS -->
                <div class="card bg-base-100 border border-base-300">
                    <div class="card-body p-4">
                        <h3 class="text-sm font-semibold opacity-70">Task details</h3>
                        <table class="table table-sm">
                            <tbody>
                                <tr>
                                    <td class="opacity-60">Story points</td>
                                    <td class="font-medium">3</td>
                                </tr>
                                <tr>
                                    <td class="opacity-60">Priority</td>
                                    <td>
                                        <div class="badge badge-secondary">1</div>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="opacity-60">Status</td>
                                    <td>
                                        <div class="badge badge-primary">ToDo</div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- DATES -->
                <div class="card bg-base-100 border border-base-300">
                    <div class="card-body p-4">
                        <h3 class="text-sm font-semibold opacity-70 mb-2">Dates</h3>
                        <table class="table table-sm">
                            <tbody>
                                <tr>
                                    <td class="opacity-60">Created</td>
                                    <td>2026-12-31</td>
                                </tr>
                                <tr>
                                    <td class="opacity-60">Due date</td>
                                    <td>2026-12-31</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- DESCRIPTION -->
                <div class="card bg-base-100 border border-base-300">
                    <div class="card-body p-4">
                        <h3 class="text-sm font-semibold opacity-70">Description</h3>
                        <p class="text-sm">Task description...</p>
                    </div>
                </div>


                <!-- CLOSE -->
                <button class="btn btn-neutral mt-auto"
                    onclick="document.getElementById('task-info-drawer').checked=false">
                    Close
                </button>

            </div>

        </div>
    </div>
</template>

<script>
</script>

<style scoped></style>