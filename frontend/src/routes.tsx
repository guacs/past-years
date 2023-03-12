import { RouteDefinition } from "@solidjs/router";
import { lazy } from "solid-js";
import QuestionData from "./pages/singleQuestion.data";

const HomePage = lazy(() => import("./pages/HomePage"));
const QuestionsPage = lazy(() => import("./pages/QuestionsPage"));
const ReportIncorrectQuestionPage = lazy(
	() => import("./pages/ReportIncorrectQuestionPage"),
);
const LoginPage = lazy(() => import("./pages/LoginPage"));
const SignUpPage = lazy(() => import("./pages/SignUpPage"));

const routes: RouteDefinition[] = [
	{
		path: "/",
		component: HomePage,
	},
	{
		path: "/questions/:pageNum?",
		component: QuestionsPage,
	},
	{
		path: "/incorrect-question/:id",
		component: ReportIncorrectQuestionPage,
		data: QuestionData,
	},
	{
		path: "/login",
		component: LoginPage,
	},
	{
		path: "/sign-up",
		component: SignUpPage,
	},
];

export default routes;
