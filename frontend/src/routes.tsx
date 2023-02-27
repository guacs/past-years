import { RouteDefinition } from "@solidjs/router";
import { lazy } from "solid-js";

const HomePage = lazy(() => import("./pages/HomePage"));
const QuestionsPage = lazy(() => import("./pages/QuestionsPage"));

const routes: RouteDefinition[] = [
	{
		path: "/",
		component: HomePage,
	},
	{
		path: "/questions",
		component: QuestionsPage,
	},
];

export default routes;
