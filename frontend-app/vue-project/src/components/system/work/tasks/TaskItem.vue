<template>
    <div class="w-full h-16 flex items-center p-2 border border-base-300 bg-base-200 hover:bg-base-300 hover:cursor-pointer"
        @click="selectTask">
        <div class="flex flex-col flex-1 px-4">
            <h1 class="font-medium text-md">{{ task.title }}</h1>
            <p class="text-xs text-base-content/60">{{ task.description }}</p>
        </div>
        <div class="pr-4 text-xs text-base-content/60">
            Due {{ task.dueDate }}
        </div>
    </div>
</template>

<script>
export default {
    name: 'TaskListItem',
    props: {
        task: {
            type: Object,
            required: true
        }
    },
    methods: {
        selectTask() {
            this.$emit('select', this.task);
        }
    }
};
</script>