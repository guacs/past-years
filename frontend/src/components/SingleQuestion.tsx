import {
	Divider,
	HStack,
	Radio,
	RadioGroup,
	Tag,
	Text,
	VStack,
} from "@hope-ui/solid";
import { For, Show } from "solid-js";
import { Answers, Question } from "../types";
import { title } from "../utils";

// ----- Props Interfaces/Types -----

/** The props to the SingleQuestion component. */
interface SingleQuestion {
	num: number; // The question number
	question: Question;
}

/** The props to the Answers component. */
interface AnswerProps {
	answers: Answers;
	correctAnswer: string;
}

// ----- Constants -----
const answerKeys = ["a", "b", "c", "d"] as const;

// ----- Components -----

/** Displays a single question. */
export default function SingleQuestion(props: SingleQuestion) {
	return (
		<>
			<VStack alignItems="left" spacing="2">
				<Text fontSize="medium" marginBottom="$5">
					{props.num}. {props.question.mainQuestion}
				</Text>
				<Show when={props.question.questionOptions.length !== 0}>
					<For each={props.question.questionOptions}>
						{(opt) => (
							<Text fontSize="medium" paddingLeft="$12" marginBottom="$5">
								{opt}
							</Text>
						)}
					</For>
				</Show>
				<Show when={props.question.continuation.length !== 0}>
					<Text fontSize="medium">{props.question.continuation}</Text>
				</Show>
				<AnswerComponent
					answers={props.question.answers}
					correctAnswer={props.question.correctAnswer}
				/>
				<HStack alignItems="left" marginTop="$5" spacing="$4">
					<Tag colorScheme="primary">{props.question.exam}</Tag>
					<Tag colorScheme="accent">{title(props.question.subject)}</Tag>
					<Tag colorScheme="warning">{props.question.year}</Tag>
				</HStack>
			</VStack>
			<Divider marginTop="$4" marginBottom="$4" />
		</>
	);
}

/** Displays the answers as well as handles dealing with whether
 * the user selected the correct answer or not.
 */
function AnswerComponent(props: AnswerProps) {
	return (
		<RadioGroup>
			<VStack marginLeft="$5" marginTop="$5" alignItems="left">
				<For each={answerKeys}>
					{(key) => {
						const color =
							key === props.correctAnswer.toLowerCase() ? "success" : "danger";

						return (
							<Radio p="$2" value={key} variant="filled" colorScheme={color}>
								{props.answers[key]}
							</Radio>
						);
					}}
				</For>
			</VStack>
		</RadioGroup>
	);
}
