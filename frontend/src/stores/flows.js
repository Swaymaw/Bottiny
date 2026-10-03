import { defineStore } from "pinia";
import api from "../api/api";

export const useFlowsStore = defineStore("flows", {
  state: () => ({ items: [] }),
  actions: {
    async fetch() {
      this.items = await api.listFlows();
    },
    async toggle(flow) {
      await api.setEnabled(flow.name, !flow.enabled);
      flow.enabled = !flow.enabled;
    },
  },
});
