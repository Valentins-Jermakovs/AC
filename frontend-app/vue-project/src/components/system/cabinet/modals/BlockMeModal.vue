<template>
    <BaseDialog v-model="localModel" :title="$t('modals.block_me.title')" :confirm-text="$t('common.confirm')"
        :cancel-text="$t('common.cancel')" @confirm="submit">
        <div class="flex flex-col w-full gap-5">
            <!-- Error message transition -->
            <Transition name="error-slide">
                <div v-if="error">
                    <h1 class="text-error mb-2">{{ error }}</h1>
                </div>
            </Transition>

            <p>{{ $t('modals.block_me.content') }}</p>
        </div>
    </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/common/BaseDialog.vue';

export default {
    name: 'BlockMeModal',
    components: { BaseDialog },

    // Props: receive v-model and error message from parent
    props: {
        modelValue: Boolean,
        error: String,
    },

    computed: {
        // Local proxy for v-model
        localModel: {
            get() {
                return this.modelValue
            },
            set(val) {
                this.$emit('update:modelValue', val)
            },
        },
    },
    methods: {
        submit() {
            this.$emit('submit')
        }
    }
}
</script>