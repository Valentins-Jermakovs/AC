<template>
    <div class="w-full bg-base-100 border border-base-300 p-2 flex
      items-center justify-between gap-5">
        <select class="select select-bordered">
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="30">30</option>
        </select>
        <div class="flex gap-5 text-sm text-base-content/60">
            <p>
                Total projects: 29
            </p>
            <p>
                Page 1 / 5
            </p>
        </div>
        <div class="flex gap-2">
            <button class="btn btn-neutral">
                <font-awesome-icon icon="fa-solid fa-arrow-left" />
            </button>
            <button class="btn btn-neutral">
                <font-awesome-icon icon="fa-solid fa-arrow-right" />
            </button>
        </div>
    </div>
</template>

<script>
</script>

<style scoped></style>