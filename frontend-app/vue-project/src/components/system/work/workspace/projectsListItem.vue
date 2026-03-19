<template>
    <div class="w-full bg-base-100 border border-base-300 rounded-box 
        flex flex-col gap-3 p-4
        hover:border-info hover:bg-base-200 transition-all duration-300">

        <!-- Header -->
        <div class="flex justify-between items-center">
            <div class="flex items-center gap-3">
                <h2 class="text-xl font-semibold">
                Project 1
            </h2>

            <!-- created at pager -->
            <p class="text-sm badge badge-neutral rounded-box">
                2026-12-12
            </p>
            </div>

            <div class="flex gap-2">
                <button class="btn btn-ghost btn-sm">
                    <font-awesome-icon icon="fa-solid fa-pen-to-square" />
                </button>

                <button class="btn btn-ghost btn-sm text-error">
                    <font-awesome-icon icon="fa-solid fa-trash" />
                </button>
            </div>
        </div>

        <!-- Description -->
        <p class="text-base-content/70">
            Lorem ipsum dolor sit amet consectetur adipisicing elit.
            Itaque velit, error inventore repudiandae voluptas similique
            eveniet minima reprehenderit quis pariatur sapiente quasi.
        </p>

        <!-- Actions -->
        <div class="flex justify-end">
            <button class="btn btn-primary btn-sm gap-2">
                <font-awesome-icon icon="fa-solid fa-arrow-right" />
                Enter project
            </button>
        </div>

    </div>

    <!-- Edit project dialog -->
    <base-dialog>
        <div class="flex flex-col w-full">
            <!-- project title -->
            <input type="text" class="input input-bordered w-full" placeholder="Project title" />
            <!-- project description -->
            <textarea class="textarea textarea-bordered w-full" placeholder="Project description"></textarea>
        </div>
    </base-dialog>

    <!-- Delete project dialog -->
    <base-dialog>
        <p>Are you sure you want to delete this project?</p>
    </base-dialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue';

export default {
    name: 'ProjectsListItem',
    components: { BaseDialog }
}
</script>

<style scoped></style>