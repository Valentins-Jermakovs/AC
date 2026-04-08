<template>
  <div class="w-full border border-base-300 bg-base-200 p-4">
    <table class="table w-full">
      <thead>
        <tr>
          <th>Creation Date</th>
          <th>Title</th>
          <th>Content</th>
          <th>Operations</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(row, index) in newsStore.news" :key="index">
          <td>{{ row.createdAt.split(' ')[0] }}</td>
          <td>{{ row.title }}</td>
          <td>
            <div>{{ truncateContent(row.content, 100) }}</div>
          </td>

          <td class="flex gap-2">
            <button class="btn btn-sm btn-info" @click="selectNews(row)">Edit</button>
            <button class="btn btn-sm btn-error" @click="openDelete(row.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

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
  </div>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useNewsStore } from '@/stores/news'

export default {
  name: 'NewsTable',
  components: { BaseDialog },
  data() {
    return {
      newsStore: useNewsStore(),
      openDeleteModal: false,
      deleteId: null,
    }
  },
  methods: {
    openDelete(row) {
      this.openDeleteModal = true
      this.deleteId = row
    },
    deleteNews() {
      this.newsStore.deleteNews(this.deleteId)
      this.openDeleteModal = false
    },
    selectNews(row) {
      this.newsStore.selectedNews = row
    },

    // -----------------------
    // truncate content and remove HTML tags
    // -----------------------
    truncateContent(content, length = 100) {
      const textOnly = content.replace(/<\/?[^>]+(>|$)/g, '') // no HTML
      if (textOnly.length <= length) return textOnly
      return textOnly.substring(0, length) + '...'
    },
  },
  mounted() {
    this.newsStore.getAllNews()
    this.newsStore.selectedNews = null
  },
}
</script>

<style scoped></style>
