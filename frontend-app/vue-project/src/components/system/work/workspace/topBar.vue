<template>

    <div class="w-full flex items-center bg-base-100 border border-base-300 p-2 gap-5 justify-between">

        <!-- Create -->
        <button class="btn btn-accent" @click="showCreateDialog = true">
            <font-awesome-icon icon="fa-solid fa-plus" />
            Create project
        </button>

        <div class="w-48"></div>

        <!-- Search -->
        <div class="flex gap-3 flex-1">

            <input v-model="store.searchQuery" type="text" class="input input-bordered w-full" placeholder="Search..."
                @keyup.enter="search" />

            <select v-model="store.searchMode" class="select select-bordered">
                <option value="all">All</option>
                <option value="title">By title</option>
            </select>

            <button class="btn btn-primary" @click="search">
                <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
            </button>

        </div>

    </div>

    <!-- Create dialog -->
    <base-dialog v-model="showCreateDialog" title="Create project" confirmText="Create" cancelText="Cancel"
        @confirm="createProject" @cancel="resetForm">

        <div class="flex flex-col w-full gap-3">

            <input v-model="newProject.title" type="text" class="input input-bordered w-full"
                placeholder="Project title" />

            <textarea v-model="newProject.description" class="textarea textarea-bordered w-full"
                placeholder="Project description"></textarea>

        </div>

    </base-dialog>

</template>

<script>
import { useWorkspaceProjectsStore } from '@/stores/workspace/projects';
import { useUserStore } from '@/stores/user';
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {

    name: 'TopBar',

    components: {
        BaseDialog
    },

    data() {
        return {

            store: useWorkspaceProjectsStore(),
            userStore: useUserStore(),

            showCreateDialog: false,

            newProject: {
                title: '',
                description: '',
            }

        }
    },

    methods: {

        async search() {

            this.store.meta.page = 1

            if (this.store.searchMode === 'all') {
                await this.store.getAllProjects()
                return
            }

            if (this.store.searchMode === 'title') {
                await this.store.getProjectsByTitle()
            }

        },

        async createProject() {

            const payload = {
                title: this.newProject.title,
                description: this.newProject.description,
                email: this.userStore.email,
            }

            if (!this.newProject.title) return

            try {
                await this.store.createProject(payload)
                this.showCreateDialog = false
            } catch (err) {
                console.error(err)
            } finally {
                this.resetForm()
            }

        },

        resetForm() {

            this.newProject = {
                title: '',
                description: '',
            }

        }

    },

    mounted() {
        this.userStore.fetchMe()
    }

}
</script>