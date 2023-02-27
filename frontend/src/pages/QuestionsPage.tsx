import { createResource, createSignal } from "solid-js";
import { fetchFilteredQuestions } from "../api";
import Questions from "../components/Questions";
import Filter from "../components/Filter";

export default function QuestionsPage() {
	const [filter, setFilter] = createSignal<string>("exams=cse&years=2022");

	const [questions] = createResource(filter, () =>
		fetchFilteredQuestions(filter()),
	);

	return (
		<>
			<Filter onSearch={setFilter} />
			<Questions questions={questions} />
		</>
	);
}
