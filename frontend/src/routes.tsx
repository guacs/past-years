import { RouteDefinition } from "@solidjs/router";
import HomePage from "./pages/HomePage";
import QuestionsPage from "./pages/QuestionsPage";

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
