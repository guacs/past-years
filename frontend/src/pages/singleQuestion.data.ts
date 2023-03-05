import { createResource } from "solid-js";
import { RouteDataFuncArgs } from "@solidjs/router";
import { fetchQuestion } from "../api";

export default function QuestionData({ params }: RouteDataFuncArgs) {
	const [question] = createResource(() => params.id, fetchQuestion);
	return question;
}
