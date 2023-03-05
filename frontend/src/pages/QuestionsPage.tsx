import { createResource, createSignal } from "solid-js";
import { fetchFilteredQuestions } from "../api";
import Questions from "../components/Questions";
import Filter from "../components/Filter";
import { useNavigate } from "@solidjs/router";

export default function QuestionsPage() {
	const [filter, setFilter] = createSignal<string>("exams=cse&years=2022");

	const navigate = useNavigate();

	function searchBasedOnFilter(newFilter: string) {
		setFilter(newFilter);
		navigate(`/questions?${newFilter}`);
	}

	const [questions] = createResource(filter, () =>
		fetchFilteredQuestions(filter()),
	);

	return (
		<>
			<Filter onSearch={searchBasedOnFilter} />
			<Questions questions={questions} />
		</>
	);
}
