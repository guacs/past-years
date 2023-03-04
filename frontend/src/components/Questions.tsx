import { For, Match, Resource, Switch } from "solid-js";
import { Question } from "../types";
import FullQuestion from "./SingleQuestion";
import { Box, Divider, SkeletonText } from "@hope-ui/solid";
import FetchError from "./FetchError";
// ----- Props Interfaces/Types -----
interface QuestionsProps {
	questions: Resource<Question[]>;
}

export default function Questions(props: QuestionsProps) {
	return (
		<Box margin="$10">
			<Switch>
				<Match when={props.questions.loading}>
					<LoadingQuestions />
				</Match>
				<Match when={props.questions.error}>
					<FetchError error={props.questions.error} />
				</Match>
				<Match when={props.questions()}>
					<For each={props.questions()}>
						{(question, idx) => (
							<FullQuestion question={question} num={idx() + 1} showMetadata />
						)}
					</For>
				</Match>
			</Switch>
		</Box>
	);
}

function LoadingQuestions() {
	return (
		<For each={Array.from(Array(5))}>
			{() => (
				<>
					<SkeletonText mt="$10" noOfLines={4} spacing="$4" />
					<Divider marginTop="$4" marginBottom="$4" />
				</>
			)}
		</For>
	);
}
