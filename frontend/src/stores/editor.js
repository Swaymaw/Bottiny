import { defineStore } from "pinia";
import { MarkerType } from "@vue-flow/core";
import { NODE_TYPES } from "../nodeTypes";
import api from "../api/api";

const edge = (source, port, target) => ({
  id: `${source}:${port}->${target}`,
  source,
  sourceHandle: port,
  target,
  style: {
    stroke: "#888",
    strokeWidth: 3,
  },
  markerEnd: { type: MarkerType.ArrowClosed },
});

function layoutGraph({
  ids,
  start,
  nextOf,
  size = () => ({ w: 300, h: 200 }),
}) {
  const children = new Map(
    ids.map((id) => [id, nextOf(id).filter((x) => ids.includes(x))]),
  );
  const parents = new Map(ids.map((id) => [id, []]));

  for (const id of ids)
    for (const child of children.get(id)) parents.get(child).push(id);

  const depth = {};
  const queue = [start];
  depth[start] = 0;

  for (let i = 0; i < queue.length; i++) {
    const id = queue[i];

    for (const child of children.get(id)) {
      const d = depth[id] + 1;

      if (depth[child] == null || d > depth[child]) {
        depth[child] = d;
        queue.push(child);
      }
    }
  }

  const unreachable = ids.filter((id) => depth[id] == null);

  let maxDepth = Math.max(0, ...Object.values(depth));

  for (const id of unreachable) depth[id] = ++maxDepth;

  const layers = [];

  for (const id of ids) {
    const d = depth[id];
    (layers[d] ??= []).push(id);
  }

  for (const layer of layers) {
    layer.sort((a, b) => {
      const pa = parents.get(a);
      const pb = parents.get(b);

      const ay =
        pa.reduce((sum, id) => sum + (layers[depth[id]]?.indexOf(id) ?? 0), 0) /
        (pa.length || 1);
      const by =
        pb.reduce((sum, id) => sum + (layers[depth[id]]?.indexOf(id) ?? 0), 0) /
        (pb.length || 1);

      return ay - by;
    });
  }

  const GAP_X = 180;
  const GAP_Y = 100;

  const columnWidths = layers.map((layer) =>
    Math.max(...layer.map((id) => size(id).w), 0),
  );

  const columnHeights = layers.map(
    (layer) =>
      layer.reduce((sum, id) => sum + size(id).h, 0) +
      GAP_Y * Math.max(0, layer.length - 1),
  );

  const totalHeight = Math.max(...columnHeights, 0);

  const positions = {};

  let x = 0;

  layers.forEach((layer, column) => {
    let y = (totalHeight - columnHeights[column]) / 2;

    for (const id of layer) {
      positions[id] = { x, y };
      y += size(id).h + GAP_Y;
    }

    x += columnWidths[column] + GAP_X;
  });

  return positions;
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
        const hasPositions = spec.nodes.every((n) => n.position);

        const layout = hasPositions
          ? {}
          : layoutGraph({
              ids: spec.nodes.map((n) => n.id),
              start: spec.start,
              nextOf: (id) =>
                spec.edges.filter((e) => e.from === id).map((e) => e.to),
              size: (id) => {
                const n = spec.nodes.find((x) => x.id === id);
                const type = NODE_TYPES[n?.type];
                if (!type) return { w: 300, h: 200 };
                return { w: 300, h: 120 + type.ports(n.config).length * 45 };
              },
            });

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
          wasAutoLaidOut: !hasPositions,
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

    computeLayout() {
      const start = this.startNodeId;
      if (!start) return null;

      const byId = Object.fromEntries(this.nodes.map((n) => [n.id, n]));
      return layoutGraph({
        ids: this.nodes.map((n) => n.id),
        start,

        nextOf: (id) => {
          const n = byId[id];
          return NODE_TYPES[n.data.type]
            .ports(n.data.config)
            .map(
              (p) =>
                this.edges.find(
                  (e) => e.source === id && e.sourceHandle === p.id,
                )?.target,
            )
            .filter(Boolean);
        },
        size: (id) => ({
          w: byId[id].dimensions?.width ?? 300,
          h: byId[id].dimensions?.height ?? 200,
        }),
      });
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
