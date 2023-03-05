import { RouteDefinition } from "@solidjs/router";
import { lazy } from "solid-js";
import QuestionData from "./pages/singleQuestion.data";

const HomePage = lazy(() => import("./pages/HomePage"));
const QuestionsPage = lazy(() => import("./pages/QuestionsPage"));
const ReportIncorrectQuestionPage = lazy(
	() => import("./pages/ReportIncorrectQuestionPage"),
);

const routes: RouteDefinition[] = [
	{
		path: "/",
		component: HomePage,
	},
	{
		path: "/questions",
		component: QuestionsPage,
	},
	{
		path: "/incorrect-question/:id",
		component: ReportIncorrectQuestionPage,
		data: QuestionData,
	},
];

export default routes;
