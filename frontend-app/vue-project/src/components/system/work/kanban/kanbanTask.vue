<template>
    <div class="w-full bg-base-100 rounded-box p-1 border border-base-300">
        <!-- Task title and dropdown menu -->
        <div class="flex flex-col items-center ">
            <div class="w-full flex justify-between items-center p-1">
                <h2 class="flex-1">{{ task.title }}</h2>
                <!-- Stage options dropdown -->
                <div class="dropdown dropdown-right z-10">
                    <div tabindex="0" role="button" class="btn btn-sm btn-ghost">⋮</div>
                    <ul tabindex="0"
                        class="dropdown-content menu bg-base-200 border border-base-300 rounded-box w-48 p-2 shadow">
                        <li>
                            <button class="flex gap-2 items-center text-blue-500">
                                <font-awesome-icon icon="fa-solid fa-pencil" />
                                Update task
                            </button>
                        </li>
                        <li>
                            <button class="flex gap-2 items-center text-green-500">
                                <font-awesome-icon icon="fa-solid fa-arrow-up" />
                                Move task up
                            </button>
                        </li>
                        <li>
                            <button class="flex gap-2 items-center text-green-500">
                                <font-awesome-icon icon="fa-solid fa-arrow-down" />
                                Move task down
                            </button>
                        </li>
                        <li>
                            <button class="flex gap-2 items-center text-purple-500">
                                <font-awesome-icon icon="fa-solid fa-arrow-right" />
                                Move task to right
                            </button>
                        </li>
                        <li>
                            <button class="flex gap-2 items-center text-purple-500">
                                <font-awesome-icon icon="fa-solid fa-arrow-left" />
                                Move task to left
                            </button>
                        </li>
                        <li>
                            <button class="flex gap-2 items-center text-red-500">
                                <font-awesome-icon icon="fa-solid fa-trash" />
                                Delete task
                            </button>
                        </li>
                    </ul>
                </div>
            </div>
            <!-- Description -->
            <div class="w-full p-1">
                <p>{{ task.description }}</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  props: { task: { type: Object, required: true } },
}
</script>

<style scoped></style>