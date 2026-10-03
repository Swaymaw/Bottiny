<script setup>
defineProps({ config: { type: Object, required: true } });
</script>

<template>
    <label class="block mb-2">
        Message
        <textarea
            v-model="config.text"
            placeholder="Print('Hello, World!')"
            class="bg-black rounded-md p-2 text-sm w-full"
            rows="4"
        />
    </label>
</template>
