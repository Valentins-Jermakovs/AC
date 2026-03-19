<template>

    <div class="drawer drawer-end">

        <input id="stage-info-drawer" type="checkbox" class="drawer-toggle" />

        <!-- CONTENT -->
        <div class="drawer-content">

            <div class="w-full bg-base-100 border border-base-300
            rounded-box p-4 flex flex-col gap-4">

                <!-- HEADER -->
                <div class="flex items-center justify-between">

                    <div class="flex items-center gap-3">

                        <h3 class="font-semibold text-lg">
                            Stage title...
                        </h3>

                        <div class="flex gap-2">

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

                    <label for="stage-info-drawer" class="btn btn-primary btn-sm gap-2">
                        <font-awesome-icon icon="fa-solid fa-bars" />
                        Info
                    </label>

                </div>

                <!-- TASKS -->
                <ProjectTaskList></ProjectTaskList>

            </div>

        </div>


        <!-- DRAWER -->
        <div class="drawer-side">

            <label for="stage-info-drawer" class="drawer-overlay"></label>

            <div class="bg-base-200 min-h-full w-96 p-6
            flex flex-col gap-6">

                <!-- TITLE -->
                <div class="flex items-center justify-between">

                    <h2 class="text-2xl font-semibold">
                        Stage info
                    </h2>

                    <button class="btn btn-ghost btn-sm btn-circle"
                        onclick="document.getElementById('stage-info-drawer').checked=false">
                        ✕
                    </button>

                </div>


                <!-- ACTIONS -->
                <div class="bg-base-100 border border-base-300
                rounded-box w-full">

                    <ul class="menu w-full">

                        <li>
                            <button class="flex gap-3">
                                <font-awesome-icon icon="fa-solid fa-plus" />
                                Add stage
                            </button>
                        </li>

                        <li>
                            <button class="flex gap-3">
                                <font-awesome-icon icon="fa-solid fa-code-branch" />
                                Add relative stage
                            </button>
                        </li>

                        <li>
                            <button class="flex gap-3">
                                <font-awesome-icon icon="fa-solid fa-pen" />
                                Edit stage
                            </button>
                        </li>

                        <li class="border-t border-base-300 mt-2 pt-2">

                            <button class="text-error flex gap-3">

                                <font-awesome-icon icon="fa-solid fa-trash" />

                                Delete stage

                            </button>

                        </li>

                    </ul>

                </div>


                <!-- DESCRIPTION -->
                <div class="card bg-base-100 border border-base-300">

                    <div class="card-body p-4">

                        <h3 class="font-semibold text-sm opacity-70">
                            Description
                        </h3>

                        <p class="text-sm">
                            Stage description here...
                        </p>

                    </div>

                </div>


                <!-- META -->
                <div class="card bg-base-100 border border-base-300">

                    <div class="card-body p-4">

                        <h3 class="font-semibold text-sm opacity-70 mb-2">
                            Metadata
                        </h3>

                        <table class="table table-sm">

                            <tbody>

                                <tr>
                                    <td class="opacity-60">Created</td>
                                    <td class="font-medium">
                                        2026-12-31
                                    </td>
                                </tr>

                                <tr>
                                    <td class="opacity-60">Due date</td>
                                    <td class="font-medium">
                                        2026-12-31
                                    </td>
                                </tr>

                            </tbody>

                        </table>

                    </div>

                </div>


                <!-- CLOSE -->
                <button class="btn btn-neutral mt-auto"
                    onclick="document.getElementById('stage-info-drawer').checked=false">
                    Close
                </button>

            </div>

        </div>

    </div>

</template>

<script>

import ProjectTaskList from './projectTaskList.vue'

export default {

    name: 'KanbanStageInfoDrawer',

    components: {
        ProjectTaskList
    }

}

</script>