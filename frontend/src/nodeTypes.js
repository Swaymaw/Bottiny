import StaticConfig from "./components/config/StaticConfig.vue";
import ButtonsConfig from "./components/config/ButtonsConfig.vue";
import LLMConfig from "./components/config/LLMConfig.vue";
import { uid } from "./utils";

export const NODE_TYPES = {
  static: {
    label: "Print",
    color: "#5a9a5a",
    config: StaticConfig,
    defaultConfig: () => ({ text: "" }),
    ports: () => [{ id: "out", label: "next" }],
    validate: (c) => (c.text.trim() ? null : "Print node needs a message"),
  },

  buttons: {
    label: "Button",
    color: "#c0436e",
    config: ButtonsConfig,
    defaultConfig: () => ({
      text: "",
      buttons: [{ id: uid("opt_"), label: "" }],
    }),
    ports: (c) =>
      c.buttons.map((b) => ({ id: b.id, label: b.label || "(empty)" })),
    validate: (c) => {
      if (!c.text.trim()) return "Button node needs a question";
      if (!c.buttons.length) return "Button node needs at least one choice";
      if (c.buttons.some((b) => !b.label.trim()))
        return "Every choice needs a label";
      return null;
    },
  },

  llm: {
    label: "LLM",
    color: "#4b4bff",
    config: LLMConfig,
    defaultConfig: () => ({ system: "", loop: true }),
    ports: (c) => (c.loop ? [] : [{ id: "out", label: "when done" }]),
  },
};
