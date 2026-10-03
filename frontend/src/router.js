import { createRouter, createWebHistory } from "vue-router";
import FlowEditorView from "./pages/FlowEditor.vue";
import Flows from "./pages/Flows.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/flows" },
    {
      path: "/flows",
      component: Flows,
      children: [{ path: ":name?", name: "editor", component: FlowEditorView }],
    },
  ],
});
