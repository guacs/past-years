import { RouteDefinition } from "@solidjs/router";
import HomePage from "./pages/HomePage";

const routes: RouteDefinition[] = [
	{
		path: "/",
		component: HomePage,
	},
];

export default routes;
