<template>
    <!-- Stage header -->
    <div class="flex items-center justify-between p-2 border border-base-300
        bg-base-100">
        <h2 class="flex-1 font-semibold text-lg">{{ stage.title }}</h2>

        <!-- Stage options dropdown -->
        <div class="dropdown dropdown-right">
            <div tabindex="0" role="button" class="btn btn-sm btn-ghost">⋮</div>
            <ul tabindex="0"
                class="dropdown-content menu bg-base-200 border border-base-300 rounded-box w-48 p-2 shadow">
                <li>
                    <button class="flex gap-2 items-center text-blue-500">
                        <font-awesome-icon icon="fa-solid fa-pencil" />
                        Update stage
                    </button>
                </li>
                <li>
                    <button class="flex gap-2 items-center text-green-500">
                        <font-awesome-icon icon="fa-solid fa-arrow-up" />
                        Insert stage before
                    </button>
                </li>
                <li>
                    <button class="flex gap-2 items-center text-green-500">
                        <font-awesome-icon icon="fa-solid fa-arrow-down" />
                        Insert stage after
                    </button>
                </li>
                <li>
                    <button class="flex gap-2 items-center text-purple-500">
                        <font-awesome-icon icon="fa-solid fa-arrow-right" />
                        Move stage to right
                    </button>
                </li>
                <li>
                    <button class="flex gap-2 items-center text-purple-500">
                        <font-awesome-icon icon="fa-solid fa-arrow-left" />
                        Move stage to left
                    </button>
                </li>
                <li>
                    <button class="flex gap-2 items-center text-red-500">
                        <font-awesome-icon icon="fa-solid fa-trash" />
                        Delete stage
                    </button>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    name: "kanbanStageTitle",
    props: {
        stage: {
            type: Object,
            required: true
        }
    }
}
</script>

<style></style>