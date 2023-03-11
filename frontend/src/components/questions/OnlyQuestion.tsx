import { Text, Radio, RadioGroup, VStack } from "@hope-ui/solid";
import { Show, For } from "solid-js";
import { AnswerProps, QuestionProps } from "./propTypes";

// ----- Constants -----
const answerKeys = ["a", "b", "c", "d"] as const;

/** Component that simply displays the question and it's answers. */
export default function OnlyQuestion(props: QuestionProps) {
	return (
		<>
			<VStack alignItems="left" spacing="2">
				<Text fontSize="medium" marginBottom="$5">
					{props.question.mainQuestion}
				</Text>
				<Show when={props.question.questionOptions.length !== 0}>
					<For each={props.question.questionOptions}>
						{(opt) => (
							<Text
								fontSize="medium"
								paddingLeft="$12"
								paddingRight="$3"
								marginBottom="$5"
							>
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
			</VStack>
		</>
	);
}

/** Displays the answers as well as handles dealing with whether
 * the user selected the correct answer or not.
 */
function AnswerComponent(props: AnswerProps) {
	return (
		<RadioGroup marginBottom="$5">
			<VStack marginLeft="$1" marginTop="$5" alignItems="left">
				<For each={answerKeys}>
					{(key) => {
						const color =
							key === props.correctAnswer.toLowerCase() ? "success" : "danger";

						return (
							<Radio
								// m="$3"
								marginTop="$2"
								p="$2"
								value={key}
								variant="filled"
								colorScheme={color}
							>
								{props.answers[key]}
							</Radio>
						);
					}}
				</For>
			</VStack>
		</RadioGroup>
	);
}
