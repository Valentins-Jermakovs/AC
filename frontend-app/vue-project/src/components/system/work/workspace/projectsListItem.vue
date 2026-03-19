<template>
    <div class="w-full bg-base-100 border border-base-300 rounded-box 
        flex flex-col gap-3 p-4
        hover:border-info hover:bg-base-200 transition-all duration-300">

        <!-- Header -->
        <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold">
                Project 1
            </h2>

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
</template>

<script>
</script>

<style scoped></style>