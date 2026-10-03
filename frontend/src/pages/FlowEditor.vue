<script setup>
import { nextTick, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { VueFlow, useVueFlow } from "@vue-flow/core";
import { Background } from "@vue-flow/background";
import FlowNode from "../components/FlowNode.vue";
import NodePicker from "../components/NodePicker.vue";
import { useEditorStore } from "../stores/editor";
import { useFlowsStore } from "../stores/flows";

const store = useEditorStore();
const flows = useFlowsStore();
const route = useRoute();
const router = useRouter();
const canvas = ref(null);

const {
    screenToFlowCoordinate,
    fitView,
    getSelectedNodes,
    getSelectedEdges,
    removeNodes,
    removeEdges,
} = useVueFlow();

watch(
    () => route.params.name,
    async (name) => {
        if (name) await store.load(name);
        else store.reset();
        await nextTick();
        setTimeout(() => fitView({ padding: 0.3, maxZoom: 1 }), 50); // wait for nodes to be measured
    },
    { immediate: true },
);

function onPick(type) {
    const { nodeId, port } = store.picker;
    if (nodeId) {
        store.addNode(type, { from: { nodeId, port } });
    } else {
        const r = canvas.value.getBoundingClientRect();
        store.addNode(type, {
            position: screenToFlowCoordinate({
                x: r.left + r.width / 2,
                y: r.top + r.height / 2,
            }),
        });
    }
    store.closePicker();
}

function deleteSelected() {
    removeEdges(getSelectedEdges.value);
    removeNodes(getSelectedNodes.value);
}

async function finish() {
    if (!(await store.save())) return;
    await flows.fetch();
    router.push({ name: "editor", params: { name: store.name } });
}
</script>

<template>
    <div
        ref="canvas"
        class="relative h-full overflow-hidden rounded-3xl bg-zinc-800"
    >
        <VueFlow
            v-model:nodes="store.nodes"
            v-model:edges="store.edges"
            :connect-on-click="false"
            :delete-key-code="['Backspace', 'Delete']"
            @connect="store.connect"
        >
            <template #node-flow="nodeProps">
                <FlowNode v-bind="nodeProps" />
            </template>

            <Background pattern-color="#2a2a2a" />
        </VueFlow>

        <div
            class="absolute left-1/2 top-5 z-10 flex -translate-x-1/2 items-center gap-4 rounded-full border border-zinc-700 bg-zinc-900/85 px-5 py-2 backdrop-blur-md"
        >
            <input
                v-model="store.name"
                :disabled="!store.isNew"
                placeholder="flow-name"
                class="w-50 rounded-full bg-transparent px-3 py-1 text-white outline-none placeholder:text-zinc-500 disabled:cursor-not-allowed disabled:opacity-60"
            />

            <span v-if="store.error" class="max-w-105 text-[13px] text-red-400">
                {{ store.error }}
            </span>
        </div>

        <div
            class="absolute bottom-5 right-5 z-10 flex items-center gap-4 rounded-full border border-zinc-700 bg-zinc-900/85 px-5 py-2 backdrop-blur-md"
        >
            <button
                @click="
                    store.openPicker({ x: $event.clientX, y: $event.clientY })
                "
                class="text-white transition-colors hover:text-zinc-300"
            >
                + Add
            </button>

            <button
                @click="deleteSelected"
                class="text-white transition-colors hover:text-red-400"
            >
                ✕ Delete
            </button>

            <button
                @click="finish"
                class="ml-6 text-white transition-colors hover:text-zinc-300"
            >
                = Finish
            </button>
        </div>

        <NodePicker
            v-if="store.picker"
            :x="store.picker.x"
            :y="store.picker.y"
            @pick="onPick"
            @close="store.closePicker"
        />
    </div>
</template>
