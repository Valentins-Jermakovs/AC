<template>
    <div class="w-full border border-base-300 bg-base-200 p-4">
        <table class="table w-full">
            <thead>
                <tr>
                    <th>Creation Date</th>
                    <th>Title</th>
                    <th>Content</th>
                    <th>Oparations</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="(row, index) in newsStore.news" :key="index">
                    <td>
                        <div>
                            {{ row.createdAt.split(' ')[0] }}
                        </div>
                    </td>

                    <td>
                        <div>
                            {{ row.title }}
                        </div>
                    </td>

                    <td>
                        <div>
                            {{ row.content }}
                        </div>
                    </td>

                    <td class="flex gap-2">
                        <button class="btn btn-sm btn-info">
                            View
                        </button>
                        <button class="btn btn-sm btn-primary">
                            Edit
                        </button>
                        <button class="btn btn-sm btn-error"
                            @click="openDelete(row.id)">
                            Delete
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- Remove News Modal -->
    <BaseDialog
    title="Delete news"
    cancel-text="cancel"
    confirm-text="delete"
    v-model="openDeleteModal"
    @confirm="deleteNews"
    >
        <p>Are you sure you want to delete this news?</p>
    </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue';
import { useNewsStore } from '@/stores/news';

export default {
    name: 'NewsTable',
    components: { BaseDialog },
    data() {
        return {
            newsStore: useNewsStore(),
            openDeleteModal: false,
            deleteId: null
        }
    },
    methods: {
        openDelete(row) {
            this.openDeleteModal = true,
            this.deleteId = row
        },
        deleteNews() {
            this.newsStore.deleteNews(this.deleteId)
            this.openDeleteModal = false
        }
    },
    mounted() {
        this.newsStore.getAllNews();
    }
}
</script>

<style scoped></style>