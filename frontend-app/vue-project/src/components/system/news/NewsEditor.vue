<template>
  <div class="p-6 border border-base-300 bg-base-200 flex flex-col gap-4">
    <!-- Title -->
    <label class="label">
      <span class="label-text">{{ $t('news.editor.title') }}:</span>
    </label>
    <input v-model="form.title" type="text" :placeholder="$t('news.editor.title_placeholder')"
      class="input input-bordered w-full" />

    <!-- Cover Image -->
    <label class="label">
      <span class="label-text">{{ $t('news.editor.image') }}:</span>
    </label>
    <input v-model="form.coverImage" type="text" :placeholder="$t('news.editor.image_placeholder')"
      class="input input-bordered w-full" />

    <!-- Tags -->
    <label class="label">
      <span class="label-text">{{ $t('news.editor.tags') }}:</span>
    </label>
    <input v-model="tagsInput" @keyup.enter="applyTags" type="text" :placeholder="$t('news.editor.tags_placeholder')"
      class="input input-bordered w-full" />

    <div class="flex gap-2 flex-wrap py-2">
      <div v-for="(tag, idx) in form.tags" :key="idx"
        class="bg-base-100 border border-base-300 gap-1 flex justify-between items-center">
        <p class="px-2">{{ tag }}</p>
        <button @click="removeTag(idx)" class="btn btn-xs btn-neutral">
          <font-awesome-icon icon="fa-solid fa-trash" />
        </button>
      </div>
    </div>

    <!-- Content -->
    <label class="label">
      <span class="label-text">{{ $t('news.editor.status.title') }}:</span>
    </label>
    <!-- Status -->
    <select v-model="form.status" class="select select-bordered w-full">
      <option value="draft">{{ $t('news.editor.status.draft') }}</option>
      <option value="published">{{ $t('news.editor.status.published') }}</option>
    </select>

    <!-- Toolbar -->
    <div class="flex gap-1 border-b border-base-300 pb-2">
      <button type="button" class="btn btn-neutral" @click="toggleBold">
        <font-awesome-icon icon="fa-solid fa-bold" />
      </button>
      <button type="button" class="btn btn-neutral" @click="toggleItalic">
        <font-awesome-icon icon="fa-solid fa-italic" />
      </button>
      <button type="button" class="btn btn-neutral" @click="toggleHeading1">H1</button>
      <button type="button" class="btn btn-neutral" @click="toggleHeading2">H2</button>
      <button type="button" class="btn btn-neutral" @click="toggleBulletList">
        <font-awesome-icon icon="fa-solid fa-list" />
      </button>
      <button type="button" class="btn btn-neutral" @click="toggleOrderedList">
        <font-awesome-icon icon="fa-solid fa-list-ol" />
      </button>
      <button type="button" class="btn btn-neutral" @click="addLink">
        <font-awesome-icon icon="fa-solid fa-link" />
      </button>
    </div>

    <label class="label">
      <span class="label-text">
        {{ $t('news.editor.content') }}:
        <small class="">{{ remainingCharacters }} / {{ maxCharacters }}</small>
      </span>
    </label>
    <!-- Editor -->
    <EditorContent :editor="editor"
      class="prose max-w-none prose-a:text-blue-600 hover:prose-a:underline border border-base-300 bg-base-100 p-2 rounded" />

    <!-- Action Buttons -->
    <div class="flex gap-2">
      <button class="btn btn-primary" @click="saveNews" :disabled="newsStore.loading">
        {{ form.id ? $t('common.update') : $t('common.create') }}
      </button>
      <button class="btn btn-secondary" @click="cancelEdit">
        {{ $t('common.cancel') }}
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="newsStore.error" class="text-red-500 text-sm">
      {{ newsStore.error }}
    </div>
  </div>
</template>

<script>
import { Editor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Link from '@tiptap/extension-link'
import { useNewsStore } from '@/stores/news'
import { useUserStore } from '@/stores/user'

export default {
  name: 'NewsEditor',
  components: { EditorContent },
  data() {
    return {
      form: {
        id: null,
        title: '',
        coverImage: '',
        tags: [],
        status: 'draft',
        content: '',
      },
      tagsInput: '',
      editor: null,
      newsStore: useNewsStore(),
      userStore: useUserStore(),
      maxCharacters: 10000,
      remainingCharacters: 10000, // sākuma vērtība
    }
  },
  mounted() {
    this.editor = new Editor({
      extensions: [StarterKit, Link],
      content: this.form.content,
      onUpdate: ({ editor }) => {
        // iegūstam plain text garumu
        let textLength = editor.state.doc.textContent.length

        // ja pārsniedz maxCharacters, griež saturu
        if (textLength > this.maxCharacters) {
          // ņem tikai pirmos maxCharacters simbolus
          const allowedText = editor.state.doc.textContent.slice(0, this.maxCharacters)
          editor.commands.setContent(allowedText)
          textLength = this.maxCharacters
        }

        this.form.content = editor.getHTML()
        this.remainingCharacters = this.maxCharacters - textLength
      },
    })

    if (this.newsStore.selectedNews) this.populateForm(this.newsStore.selectedNews)
  },
  beforeUnmount() {
    if (this.editor) this.editor.destroy()
  },
  watch: {
    'newsStore.selectedNews'(val) {
      if (val) this.populateForm(val)
      else this.resetForm()
    },
  },
  methods: {
    populateForm(news) {
      this.form = { ...this.form, ...news }
      this.editor.commands.setContent(this.form.content)
    },
    resetForm() {
      this.form = { id: null, title: '', coverImage: '', tags: [], status: 'draft', content: '' }
      this.editor.commands.clearContent()
    },
    applyTags() {
      if (!this.tagsInput.trim()) return
      const newTags = this.tagsInput
        .split(',')
        .map((t) => t.trim())
        .filter(Boolean)
      this.form.tags.push(...newTags)
      this.tagsInput = ''
    },
    removeTag(idx) {
      this.form.tags.splice(idx, 1)
    },
    async saveNews() {
      const payload = { authorEmail: this.userStore.email, ...this.form }
      if (this.form.id) {
        payload.newsId = this.form.id
        await this.newsStore.updateNews(payload)
      } else {
        await this.newsStore.createNews(payload)
      }
      this.newsStore.selectedNews = null
      this.resetForm()
    },
    cancelEdit() {
      this.newsStore.selectedNews = null
      this.resetForm()
    },
    // Toolbar actions
    toggleBold() {
      this.editor.chain().focus().toggleBold().run()
    },
    toggleItalic() {
      this.editor.chain().focus().toggleItalic().run()
    },
    toggleHeading1() {
      this.editor.chain().focus().toggleHeading({ level: 1 }).run()
    },
    toggleHeading2() {
      this.editor.chain().focus().toggleHeading({ level: 2 }).run()
    },
    toggleBulletList() {
      this.editor.chain().focus().toggleBulletList().run()
    },
    toggleOrderedList() {
      this.editor.chain().focus().toggleOrderedList().run()
    },
    addLink() {
      const url = prompt('Enter URL')
      if (url)
        this.editor
          .chain()
          .focus()
          .extendMarkRange('link')
          .setLink({ href: url, target: '_blank' })
          .run()
    },
  },
}
</script>

<style scoped>
.editor-content {
  min-height: 250px;
  outline: none;
}

.editor-content {
  min-height: 250px;
  outline: none;
}

/* Headings */
.editor-content h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.editor-content h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.editor-content h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

/* Paragraphs */
.editor-content p {
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

/* Lists */
.editor-content ul {
  list-style: disc;
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

.editor-content ol {
  list-style: decimal;
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

.editor-content li {
  margin-bottom: 0.5rem;
}

/* Links */
.editor-content a {
  color: #2563eb;
  text-decoration: underline;
}

.editor-content a:hover {
  color: #1e40af;
}
</style>
