import { Divider, Flex, Text, VStack } from "@hope-ui/solid";

import OnlyQuestion from "./questions/OnlyQuestion";
import QuestionMetadata from "./questions/QuestionMetadata";
import { FullQuestionProps } from "./questions/propTypes";
import { Show } from "solid-js";

/** Displays a single question including it's metadata. */
export default function FullQuestion(props: FullQuestionProps) {
	return (
		<>
			<VStack alignItems="left" spacing="2">
				<Flex>
					<Text marginRight="$2" fontSize="medium" as={"p"}>
						{props.num}.
					</Text>
					<OnlyQuestion question={props.question} />
				</Flex>
				<Show when={props.showMetadata}>
					<QuestionMetadata question={props.question} />
				</Show>
			</VStack>
			<Divider marginTop="$4" marginBottom="$4" />
		</>
	);
}
