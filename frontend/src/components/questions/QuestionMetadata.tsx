import {
	Flex,
	Box,
	Tag,
	Spacer,
	IconButton,
	Menu,
	MenuContent,
	MenuItem,
	MenuTrigger,
} from "@hope-ui/solid";
import { title } from "../../utils";
import { QuestionProps } from "./propTypes";
import { useNavigate } from "@solidjs/router";
import { FaSolidEllipsisVertical, FaSolidQuestion } from "solid-icons/fa";

/** Displays the metadata regarding a single question. */
export default function QuestionMetadata(props: QuestionProps) {
	return (
		<Flex marginTop="$3">
			<Box>
				<Tag m="$2" colorScheme="primary">
					{props.question.exam}
				</Tag>
				<Tag m="$2" colorScheme="accent">
					{title(props.question.subject)}
				</Tag>
				<Tag m="$2" colorScheme="warning">
					{props.question.year}
				</Tag>
			</Box>
			<Spacer />
			<QuestionSubMenu question={props.question} />
		</Flex>
	);
}

/** Displays the sub menu for a single question. */
function QuestionSubMenu(props: QuestionProps) {
	const navigate = useNavigate();

	function navigateToIncorrectQuestionPage() {
		navigate(`/incorrect-question/${props.question.id}`, {
			resolve: false,
		});
	}

	return (
		<>
			<Menu>
				<MenuTrigger
					as={IconButton}
					variant="ghost"
					colorScheme="neutral"
					icon={<FaSolidEllipsisVertical />}
					_focus={{
						boxShadow: "none",
					}}
				/>
				<MenuContent>
					<MenuItem onSelect={navigateToIncorrectQuestionPage}>
						<Flex alignItems="center" justifyContent="space-evenly">
							<FaSolidQuestion />
							Incorrect Question
						</Flex>
					</MenuItem>
				</MenuContent>
			</Menu>
		</>
	);
}
