import axios from "axios";

class Api {
  constructor(baseURL) {
    this.client = axios.create({
      baseURL: baseURL,
      headers: {
        "Content-Type": "application/json",
      },
    });
    this.client.interceptors.response.use(
      (response) => response, // success handler
      (error) => {
        // error handler
        const detail = error.response?.data?.detail;
        const status = error.response?.status;

        throw new Error(
          typeof detail === "string"
            ? detail
            : `Request failed (${status ?? "network error"})`,
        );
      },
    );
  }

  async listFlows() {
    const { data } = await this.client.get("/flows");
    return data;
  }

  async getFlow(name) {
    const { data } = await this.client.get(
      `/flows/${encodeURIComponent(name)}`,
    );
    return data;
  }

  async saveFlow(spec) {
    const { data } = await this.client.post("/flows", spec);
    return data;
  }

  async setEnabled(name, on) {
    const action = on ? "enable" : "disable";
    const { data } = await this.client.post(
      `/flows/${encodeURIComponent(name)}/${action}`,
    );
    return data;
  }
}

export default new Api("/api/v1");
