import { createSignal } from "solid-js";

const [routing, setRouting] = createSignal<boolean>(false);

export { routing, setRouting };
