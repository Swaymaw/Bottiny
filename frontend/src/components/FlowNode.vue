<script setup>
import { computed, nextTick, watch } from "vue";
import { Handle, Position, useVueFlow } from "@vue-flow/core";
import { NODE_TYPES } from "../nodeTypes";
import { useEditorStore } from "../stores/editor";
import PortRow from "./PortRow.vue";

const props = defineProps({
    id: { type: String, required: true },
    data: { type: Object, required: true },
    selected: Boolean,
});

const store = useEditorStore();
const { updateNodeInternals } = useVueFlow();

const def = computed(() => NODE_TYPES[props.data.type]);
const ports = computed(() => def.value.ports(props.data.config));
const isStart = computed(() => store.startNodeId === props.id);

watch(
    () => ports.value.map((p) => p.id).join(","),
    async (now, before) => {
        const current = now.split(",");
        before
            .split(",")
            .filter((id) => id && !current.includes(id))
            .forEach((id) => store.removeEdgesFrom(props.id, id));
        await nextTick();
        updateNodeInternals([props.id]);
    },
);
</script>

<template>
    <div
        class="w-auto rounded-3xl border-2 text-white bg-zinc-900"
        :class="{ 'shadow-[5px_5px_10px_10px_#111111]': selected }"
        :style="{ '--c': def.color }"
    >
        <Handle
            type="target"
            :position="Position.Left"
            class="-left-1.5 h-5! w-5! border-3! border-white! bg-(--c)!"
        />

        <div class="nodrag px-4 pt-4 pb-1.5">
            <component :is="def.config" :config="data.config" />
        </div>

        <PortRow v-for="p in ports" :key="p.id" :node-id="id" :port="p" />

        <div
            class="mt-1.5 inline-flex items-center gap-2.5 rounded-tr-[14px] rounded-bl-[17px] bg-(--c) px-5.5 py-1.5 pl-6.5 text-lg"
        >
            {{ def.label }}

            <button
                class="nodrag border-0 bg-transparent p-0 text-lg text-white/40"
                :class="{ 'text-yellow-400': isStart }"
                title="Set as start node"
                @click="store.startId = id"
            >
                ★
            </button>
        </div>
    </div>
</template>
