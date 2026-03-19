<template>

    <div class="w-full bg-base-100 border border-base-300 rounded-box 
flex flex-col gap-3 p-4
hover:border-info hover:bg-base-200 transition-all duration-300">

        <!-- Header -->
        <div class="flex justify-between items-center">

            <div class="flex items-center gap-3">

                <h2 class="text-xl font-semibold">
                    {{ project.title }}
                </h2>

                <p class="text-sm badge badge-neutral rounded-box">
                    {{ project.createdAt }}
                </p>

            </div>

            <div class="flex gap-2">

                <button class="btn btn-ghost btn-sm" @click="openEdit">
                    <font-awesome-icon icon="fa-solid fa-pen-to-square" />
                </button>

                <button class="btn btn-ghost btn-sm text-error" @click="openDelete">
                    <font-awesome-icon icon="fa-solid fa-trash" />
                </button>

            </div>

        </div>

        <!-- Description -->
        <p class="text-base-content/70">
            {{ project.description }}
        </p>

        <!-- Actions -->
        <div class="flex justify-end">

            <button class="btn btn-primary btn-sm gap-2">

                <font-awesome-icon icon="fa-solid fa-arrow-right" />

                Enter project

            </button>

        </div>

    </div>

    <!-- EDIT -->
    <base-dialog v-model="showEdit" title="Edit project" confirmText="Save" cancelText="Cancel" @confirm="updateProject"
        @cancel="resetEdit">

        <div class="flex flex-col w-full gap-3">

            <input v-model="editProject.title" type="text" class="input input-bordered" />

            <textarea v-model="editProject.description" class="textarea textarea-bordered"></textarea>

        </div>

    </base-dialog>

    <!-- DELETE -->
    <base-dialog v-model="showDelete" title="Delete project" confirmText="Delete" cancelText="Cancel"
        @confirm="deleteProject">

        <p>
            Are you sure you want to delete this project?
        </p>

    </base-dialog>

</template>

<script>

import { useWorkspaceProjectsStore } from '@/stores/workspace/projects';
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {

    name: 'ProjectsListItem',

    components: {
        BaseDialog
    },

    props: {
        project: {
            type: Object,
            required: true
        }
    },

    data() {

        return {

            store: useWorkspaceProjectsStore(),

            showEdit: false,
            showDelete: false,

            editProject: {
                title: '',
                description: '',
                projectId: ''
            }

        }

    },

    methods: {

        openEdit() {

            this.editProject = {

                title: this.project.title,
                description: this.project.description,
                projectId: this.project.id

            }

            this.showEdit = true

        },

        openDelete() {

            this.showDelete = true

        },

        async updateProject() {

            await this.store.updateProject(this.editProject)

            this.showEdit = false

        },

        async deleteProject() {

            await this.store.deleteProject({

                projectId: this.project.id

            })

            this.showDelete = false

        },

        resetEdit() {

            this.editProject = {
                title: '',
                description: '',
                projectId: ''
            }

        }

    }

}
</script>