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
    updateNode,
} = useVueFlow();

watch(
    () => route.params.name,
    async (name) => {
        if (name) await store.load(name);
        else store.reset();
        await nextTick();
        setTimeout(
            () => fitView({ padding: 0.3, minZoom: 0.1, maxZoom: 4.0 }),
            50,
        );
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

function autoArrange() {
    const positions = store.computeLayout();
    if (!positions) return;
    for (const [id, position] of Object.entries(positions))
        updateNode(id, { position });
    nextTick(() =>
        fitView({ padding: 0.3, minZoom: 0.1, maxZoom: 4.0, duration: 300 }),
    );
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
            min-zoom="0.10"
            max-zoom="4"
            v-model:nodes="store.nodes"
            v-model:edges="store.edges"
            :connect-on-click="true"
            :delete-key-code="['Backspace', 'Delete']"
            @connect="store.connect"
        >
            <template #node-flow="nodeProps">
                <FlowNode v-bind="nodeProps" />
            </template>

            <Background pattern-color="#666" gap="24" size="3" />
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
            class="absolute bottom-5 right-5 z-10 flex items-center gap-2 rounded-full glass"
        >
            <button
                class="rounded-full px-4 py-1.5 text-white/80 transition-colors hover:bg-blue-500/25 hover:text-blue-300"
                @click="autoArrange"
            >
                ⊞ Arrange
            </button>
            <button
                class="rounded-full px-4 py-1.5 text-white/80 transition-colors hover:bg-green-500/25 hover:text-green-300"
                @click="
                    store.openPicker({
                        x: $event.clientX - 30,
                        y: $event.clientY - 160,
                    })
                "
            >
                + Add
            </button>

            <button
                class="rounded-full px-4 py-1.5 text-white/80 transition-colors hover:bg-red-500/25 hover:text-red-300"
                @click="deleteSelected"
            >
                ✕ Delete
            </button>

            <span class="mx-1 h-5 w-px bg-white/20" />

            <button
                class="rounded-full bg-white/15 px-4 py-1.5 text-white transition-colors hover:bg-white/30"
                @click="finish"
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
