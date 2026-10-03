<script setup>
import { computed } from "vue";
import { Handle, Position } from "@vue-flow/core";
import { useEditorStore } from "../stores/editor";

const props = defineProps({
    nodeId: { type: String, required: true },
    port: { type: Object, required: true }, // { id, label }
});

const store = useEditorStore();
const connected = computed(() => store.hasEdge(props.nodeId, props.port.id));

const openPicker = (e) =>
    store.openPicker({
        nodeId: props.nodeId,
        port: props.port.id,
        x: e.clientX,
        y: e.clientY,
    });
</script>

<template>
    <div
        class="group relative flex justify-end border-t border-[#333] px-4 py-2 text-[13px] text-[#ccc]"
    >
        <span class="border-3 border-dotted pl-3 pr-3 pt-1 pb-1 rounded-lg">
            {{ port.label }}
        </span>

        <button
            v-if="!connected"
            class="nodrag absolute -right-13 top-0 flex h-full w-9 items-center justify-center opacity-0 transition-opacity duration-150 group-hover:opacity-100"
            title="Add next node"
            @click.stop="openPicker"
        >
            <span
                class="flex h-6.5 w-6.5 items-center justify-center rounded-full border-0 bg-(--c) text-base leading-none text-white"
            >
                +
            </span>
        </button>

        <Handle
            :id="port.id"
            type="source"
            :position="Position.Right"
            class="h-5! w-5! border-2! border-white! bg-(--c)!"
        />
    </div>
</template>
