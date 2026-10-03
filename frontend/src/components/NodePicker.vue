<script setup>
import { NODE_TYPES } from "../nodeTypes";

const props = defineProps({ x: Number, y: Number });
const emit = defineEmits(["pick", "close"]);

const left = Math.min(props.x, window.innerWidth - 190);
const top = Math.min(props.y, window.innerHeight - 190);
</script>

<template>
    <div class="fixed inset-0 z-50" @click="emit('close')" />

    <ul
        class="fixed z-50 min-w-40 overflow-hidden rounded-lg glass"
        :style="{ left: `${left}px`, top: `${top}px` }"
    >
        <li
            v-for="(def, type) in NODE_TYPES"
            :key="type"
            class="flex cursor-pointer items-center gap-2 rounded-md px-3 py-2 text-sm text-white/80 transition-colors hover:bg-white/10 hover:text-white border-b border-[#444]"
            :style="{ '--c': def.color }"
            @click="emit('pick', type)"
        >
            <img
                :src="def.logo"
                class="h-8 w-8 shrink-0 bg-(--c) rounded-full p-1.5"
            />

            <span class="ml-2">{{ def.label }}</span>
        </li>
    </ul>
</template>
