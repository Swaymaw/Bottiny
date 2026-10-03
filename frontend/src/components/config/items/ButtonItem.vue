<script setup>
defineProps({ button: { type: Object, required: true } });
defineEmits(["remove"]);
</script>

<template>
    <div class="flex items-center gap-2 mb-2">
        <input
            v-model="button.label"
            placeholder="Button label"
            class="flex-1 min-w-0 border-2 rounded-md text-sm px-2 py-1"
        />
        <button
            title="Remove choice"
            @click="$emit('remove')"
            class="w-8 shrink-0"
        >
            ×
        </button>
    </div>
</template>
