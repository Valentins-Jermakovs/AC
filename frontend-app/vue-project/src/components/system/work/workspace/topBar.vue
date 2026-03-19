<template>
    <div class="w-full flex items-center bg-base-100 border border-base-300 p-2 gap-5
      justify-between">
        <button class=" btn btn-accent">
            <font-awesome-icon icon="fa-solid fa-plus" />
            Create project
        </button>
        <div class="w-48"></div>
        <div class="flex gap-5 flex-1">
            <input type="text" class="input input-bordered w-full" placeholder="Search..." />
            <select class=" select">
                <option value="all">All</option>
                <option value="title">By title</option>
            </select>
            <button class="btn btn-primary">
                <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
            </button>
        </div>
    </div>
</template>

<script>
</script>

<style scoped></style>