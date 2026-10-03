<script setup>
defineProps({ config: { type: Object, required: true } });
</script>

<template>
    <div>
        <label class="block mb-2">
            Prompt
            <textarea
                class="bg-black rounded-md p-2 text-sm w-full mt-3"
                v-model="config.system"
                rows="5"
                placeholder="Prompt Here (empty = backend default)"
            />
        </label>
        <label class="text-xs flex gap-3 border-t border-[#333] pt-5">
            <input v-model="config.loop" type="checkbox" />
            <p>Keep chatting (loop). Turn off to continue to another node.</p>
        </label>
    </div>
</template>
