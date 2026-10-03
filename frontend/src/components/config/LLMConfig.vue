<script setup>
defineProps({ config: { type: Object, required: true } });
</script>

<template>
    <div>
        <label class="block mb-2">
            Prompt
            <textarea
                class="bg-black rounded-md p-2 text-sm w-full"
                v-model="config.system"
                placeholder="Prompt Here (empty = backend default)"
            />
        </label>
        <hr class="border-t-4 border-dashed border-gray-300 mb-4" />
        <label class="text-xs flex gap-3">
            <input v-model="config.loop" type="checkbox" />
            <p>Keep chatting (loop). Turn off to continue to another node.</p>
        </label>
    </div>
</template>
