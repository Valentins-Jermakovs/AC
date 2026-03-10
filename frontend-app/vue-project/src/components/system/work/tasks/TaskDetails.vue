<template>
  <div class="border border-base-300 rounded-box p-4 bg-base-100 flex flex-col gap-5 h-full">

    <!-- Title & Metadata -->
    <div class="flex flex-col gap-5">
      <h1 class="font-semibold text-2xl">{{ task.title }}</h1>
      <div class="flex flex-wrap gap-4 text-sm text-base-content/70">
        <div class="flex gap-1 items-center">
          <span class="font-medium">Status:</span>
          <span :class="statusClass(task.completed)">
            {{ task.completed ? 'Completed' : 'Pending' }}
          </span>
        </div>
        <div class="flex gap-1 items-center">
          <span class="font-medium">Created:</span>
          <span class="text-info">{{ task.createdAt }}</span>
        </div>
        <div class="flex gap-1 items-center">
          <span class="font-medium">Due date:</span>
          <span class="text-warning">{{ task.dueDate }}</span>
        </div>
      </div>
    </div>

    <!-- Description -->
    <div>
      <p class="text-base text-base-content/70">{{ task.description }}</p>
      <div class="divider"></div>
    </div>

    <div class="flex-1"></div>

    <!-- Action Buttons -->
    <div class="flex flex-wrap justify-end gap-2 mt-2">
      <button class="btn btn-md btn-error">Delete</button>
      <button class="btn btn-md btn-success">Complete</button>
      <button class="btn btn-md btn-secondary">Edit</button>
      <button class="btn btn-md btn-primary">Create new</button>
    </div>

  </div>
</template>

<script>
export default {
  name: 'TaskCard',
  props: {
    task: {
      type: Object,
      required: true
    }
  },
  methods: {
    statusClass(completed) {
      return completed
        ? 'px-2 py-0.5 rounded-full bg-green-100 text-green-800 text-xs'
        : 'px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 text-xs';
    }
  }
};
</script>