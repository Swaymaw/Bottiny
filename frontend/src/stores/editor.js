import { defineStore } from "pinia";
import { MarkerType } from "@vue-flow/core";
import { NODE_TYPES } from "../nodeTypes";
import api from "../api/api";

const edge = (source, port, target) => ({
  id: `${source}:${port}->${target}`,
  source,
  sourceHandle: port,
  target,
  type: "smoothstep",
  markerEnd: { type: MarkerType.ArrowClosed, color: "#888" },
});

function autoLayout(spec) {
  const depth = { [spec.start]: 0 };
  const queue = [spec.start];
  while (queue.length) {
    const cur = queue.shift();
    for (const e of spec.edges) {
      if (e.from === cur && !(e.to in depth)) {
        depth[e.to] = depth[cur] + 1;
        queue.push(e.to);
      }
    }
  }
  const rows = {};
  return Object.fromEntries(
    spec.nodes.map((n) => {
      const d = depth[n.id] ?? 0;
      rows[d] = (rows[d] ?? -1) + 1;
      return [n.id, { x: d * 380, y: rows[d] * 220 }];
    }),
  );
}

const stripEmpty = (config) =>
  Object.fromEntries(Object.entries(config).filter(([, v]) => v !== ""));

export const useEditorStore = defineStore("editor", {
  state: () => ({
    name: "",
    isNew: true,
    startId: null,
    nodes: [],
    edges: [],
    picker: null,
    error: null,
  }),

  getters: {
    startNodeId: (s) =>
      s.nodes.some((n) => n.id === s.startId)
        ? s.startId
        : (s.nodes[0]?.id ?? null),
  },

  actions: {
    reset() {
      Object.assign(this, {
        name: "",
        isNew: true,
        startId: null,
        nodes: [],
        edges: [],
        picker: null,
        error: null,
      });
      this.addNode("static", { position: { x: 80, y: 80 } });
    },

    async load(name) {
      this.error = null;
      try {
        const { spec } = await api.getFlow(name);
        const layout = autoLayout(spec);
        this.nodes = spec.nodes.map((n) => {
          if (!NODE_TYPES[n.type])
            throw new Error(`Unknown node type "${n.type}"`);
          return {
            id: n.id,
            type: "flow",
            position: n.position ?? layout[n.id],
            data: {
              type: n.type,
              config: { ...NODE_TYPES[n.type].defaultConfig(), ...n.config },
            },
          };
        });
        this.edges = spec.edges.map((e) => edge(e.from, e.port, e.to));
        Object.assign(this, {
          name,
          isNew: false,
          startId: spec.start,
          picker: null,
        });
      } catch (e) {
        this.error = e.message;
      }
    },

    newId(type) {
      let n = 1;
      while (this.nodes.some((x) => x.id === `${type}_${n}`)) n++;
      return `${type}_${n}`;
    },

    addNode(type, { position, from } = {}) {
      const id = this.newId(type);
      if (from) {
        const src = this.nodes.find((n) => n.id === from.nodeId);
        const ports = NODE_TYPES[src.data.type].ports(src.data.config);
        const row = ports.findIndex((p) => p.id === from.port);
        position = {
          x: src.position.x + (src.dimensions?.width ?? 300) + 120,
          y: src.position.y + row * 150,
        };
      }
      this.nodes.push({
        id,
        type: "flow",
        position,
        data: { type, config: NODE_TYPES[type].defaultConfig() },
      });
      if (!this.startId) this.startId = id;
      if (from)
        this.connect({
          source: from.nodeId,
          sourceHandle: from.port,
          target: id,
        });
    },

    connect({ source, sourceHandle, target }) {
      this.edges = this.edges.filter(
        (e) => !(e.source === source && e.sourceHandle === sourceHandle),
      );
      this.edges.push(edge(source, sourceHandle, target));
    },

    removeEdgesFrom(nodeId, port) {
      this.edges = this.edges.filter(
        (e) => !(e.source === nodeId && e.sourceHandle === port),
      );
    },

    hasEdge(nodeId, port) {
      return this.edges.some(
        (e) => e.source === nodeId && e.sourceHandle === port,
      );
    },

    openPicker(picker) {
      this.picker = picker;
    },
    closePicker() {
      this.picker = null;
    },

    toSpec() {
      return {
        name: this.name,
        start: this.startNodeId,
        nodes: this.nodes.map((n) => ({
          id: n.id,
          type: n.data.type,
          config: stripEmpty(n.data.config),
          position: {
            x: Math.round(n.position.x),
            y: Math.round(n.position.y),
          },
        })),
        edges: this.edges.map((e) => ({
          from: e.source,
          port: e.sourceHandle,
          to: e.target,
        })),
      };
    },

    validate() {
      if (!/^[\w-]+$/.test(this.name))
        return "Flow name: letters, numbers, - and _ only";
      if (!this.startNodeId) return "Add at least one node";
      for (const n of this.nodes) {
        const err = NODE_TYPES[n.data.type].validate?.(n.data.config);
        if (err) return `${n.id}: ${err}`;
      }
      return null;
    },

    async save() {
      this.name = this.name.trim();
      this.error = this.validate();
      if (this.error) return false;
      try {
        await api.saveFlow(this.toSpec());
        this.isNew = false;
        return true;
      } catch (e) {
        this.error = e.message;
        return false;
      }
    },
  },
});
