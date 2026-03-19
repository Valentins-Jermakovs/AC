<template>
  <div class="drawer drawer-end">

    <input
      :id="'task-info-drawer-' + task.id"
      type="checkbox"
      class="drawer-toggle"
    />

    <!-- CONTENT -->
    <div class="drawer-content">
      <div
        class="w-full bg-base-100 border border-base-300 rounded-box p-3 flex items-center justify-between"
      >

        <!-- LEFT -->
        <div class="flex gap-2 flex-1">

          <div class="flex items-center gap-3">
            <h3 class="font-medium">
              {{ task.title }}
            </h3>

            <div class="badge badge-primary badge-outline">
              Status: {{ task.status }}
            </div>
          </div>

          <!-- META -->
          <div class="flex flex-wrap gap-2 text-xs">

            <div class="badge badge-neutral gap-2">
              SP: {{ task.storyPoints }}
            </div>

            <div class="badge badge-secondary gap-2">
              Priority: {{ task.priority }}
            </div>

            <div class="badge badge-neutral gap-2">
              {{ task.createdAt }}
            </div>

            <div class="badge badge-warning gap-2">
              {{ task.dueDate }}
            </div>

          </div>

        </div>

        <!-- OPEN -->
        <label
          :for="'task-info-drawer-' + task.id"
          class="btn btn-primary btn-sm"
        >
          Info
        </label>

      </div>
    </div>


    <!-- DRAWER -->
    <div class="drawer-side">

      <label
        :for="'task-info-drawer-' + task.id"
        class="drawer-overlay"
      ></label>


      <div class="bg-base-200 min-h-full w-96 p-6 flex flex-col gap-6">

        <!-- HEADER -->
        <div class="flex justify-between">

          <h2 class="text-xl font-semibold">
            {{ task.title }}
          </h2>

          <label
            :for="'task-info-drawer-' + task.id"
            class="btn btn-ghost btn-sm btn-circle"
          >
            ✕
          </label>

        </div>


        <!-- DETAILS -->
        <div class="card bg-base-100 border">

          <div class="card-body p-4">

            <h3 class="text-sm font-semibold opacity-70">
              Task details
            </h3>

            <table class="table table-sm">

              <tbody>

                <tr>
                  <td>Story points</td>
                  <td>{{ task.storyPoints }}</td>
                </tr>

                <tr>
                  <td>Priority</td>
                  <td>
                    <div class="badge badge-secondary">
                      {{ task.priority }}
                    </div>
                  </td>
                </tr>

                <tr>
                  <td>Status</td>
                  <td>
                    <div class="badge badge-primary">
                      {{ task.status }}
                    </div>
                  </td>
                </tr>

              </tbody>

            </table>

          </div>

        </div>


        <!-- DATES -->
        <div class="card bg-base-100 border">

          <div class="card-body p-4">

            <h3 class="text-sm font-semibold opacity-70">
              Dates
            </h3>

            <table class="table table-sm">

              <tbody>

                <tr>
                  <td>Created</td>
                  <td>{{ task.createdAt }}</td>
                </tr>

                <tr>
                  <td>Due</td>
                  <td>{{ task.dueDate }}</td>
                </tr>

              </tbody>

            </table>

          </div>

        </div>


        <!-- DESCRIPTION -->
        <div class="card bg-base-100 border">

          <div class="card-body p-4">

            <h3 class="text-sm font-semibold opacity-70">
              Description
            </h3>

            <p class="text-sm">
              {{ task.description || 'No description' }}
            </p>

          </div>

        </div>


        <!-- CLOSE -->
        <label
          :for="'task-info-drawer-' + task.id"
          class="btn btn-neutral mt-auto"
        >
          Close
        </label>

      </div>

    </div>

  </div>
</template>

<script>
export default {

  name: 'ProjectTask',

  props: {
    task: {
      type: Object,
      required: true
    }
  }

}
</script>