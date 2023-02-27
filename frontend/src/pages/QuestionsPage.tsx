import { createResource } from "solid-js";
import { fetchFilteredQuestions } from "../api";
import Questions from "../components/Questions";

export default function QuestionsPage() {
	const [questions] = createResource(() => fetchFilteredQuestions(""));

	return (
		<>
			<Questions questions={questions} />
		</>
	);
}
