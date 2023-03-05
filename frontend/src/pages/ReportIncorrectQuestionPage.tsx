import { useParams, useRouteData } from "@solidjs/router";
import {
	Match,
	Show,
	Switch,
	batch,
	createResource,
	createSignal,
} from "solid-js";
import QuestionData from "./singleQuestion.data";
import {
	Alert,
	AlertDescription,
	AlertIcon,
	AlertTitle,
	Anchor,
	Box,
	Button,
	Center,
	Flex,
	FormControl,
	FormErrorMessage,
	Heading,
	Text,
	Textarea,
} from "@hope-ui/solid";
import FetchError from "../components/FetchError";
import OnlyQuestion from "../components/questions/OnlyQuestion";
import QuestionMetadata from "../components/questions/QuestionMetadata";
import { fetchIncorrectQuestionUrl, reportIncorrectQuestion } from "../api";
import LoadingQuestion from "../components/questions/LoadingQuestion";

export default function ReportIncorrectQuestionPage() {
	const question = useRouteData<typeof QuestionData>();
	const params = useParams();

	const [userComments, setUserComments] = createSignal<string>("");
	const [reporting, setReporting] = createSignal<boolean>(false);
	const [reportSuccess, setReportSuccess] = createSignal<boolean | null>(null);
	const [invalidComment, setInvalidComment] = createSignal<boolean>(false);

	/** The URL of the comment in the GitHub issues which shows
	 * the user's comments.
	 *
	 * NOTE: This is different from the `issuesUrl`.
	 */
	const [userCommentUrl, setUserCommentUrl] = createSignal<string>("");

	const [issuesUrl] = createResource(
		() => fetchIncorrectQuestionUrl(params.id),
		{
			initialValue: "",
		},
	);

	/** Calls the API to report the question as potentially incorrect. */
	function reportQuestion() {
		if (!userComments()) {
			setInvalidComment(true);
			return;
		}

		batch(() => {
			setInvalidComment(false);
			setReporting(true);
		});

		const _question = question();
		const questionId = _question ? _question.id : "";
		reportIncorrectQuestion(questionId, userComments())
			.then((url) => {
				batch(() => {
					setReporting(false);
					setUserCommentUrl(url);
					setReportSuccess(true);
				});
			})
			.catch(() => {
				batch(() => {
					setReporting(false);
					setReportSuccess(true);
				});
			});
	}

	/** A wrapper to stop typescript from complaining
	 * about the potentially undefined type even though
	 * it is checked in the Match component.
	 */
	function getQuestion() {
		const _question = question();
		if (_question !== undefined) {
			return (
				<>
					<Flex>
						<Text marginRight="$2" fontSize="medium" as={"p"}>
							Q.
						</Text>
						<OnlyQuestion question={_question} />
					</Flex>
					<QuestionMetadata question={_question} />
				</>
			);
		}
		return undefined;
	}

	return (
		<Box margin="$10" marginLeft="$28" marginRight="$28">
			<Center>
				<Heading fontSize="$4xl">Report Incorrect Question</Heading>
			</Center>
			<Box marginBottom="$10">
				<Switch>
					<Match when={question.loading}>
						<LoadingQuestion />
					</Match>
					<Match when={question.error}>
						<FetchError error={question.error} />
					</Match>
					<Match when={question()}>
						<Box margin="$10">{getQuestion()}</Box>
						<Show when={userCommentUrl()}>
							<Text>
								You can track this issue{" "}
								<Anchor external href={userCommentUrl()} color="blue">
									here
								</Anchor>
							</Text>
						</Show>
					</Match>
				</Switch>
			</Box>
			<FormControl invalid={invalidComment()}>
				<Textarea
					placeholder="Describe the problem"
					value={userComments()}
					onChange={(e) => setUserComments(e.currentTarget.value)}
				/>
				<FormErrorMessage>This is required.</FormErrorMessage>
			</FormControl>
			<Box marginTop="$4" marginBottom="$4">
				<Show when={!issuesUrl.error && issuesUrl()}>
					<Text>
						Known issues can be seen{" "}
						<Anchor href={issuesUrl()} color="$info9" external>
							here
						</Anchor>
					</Text>
				</Show>
			</Box>
			<Box marginBottom="$24">
				<Button
					loading={reporting()}
					onClick={reportQuestion}
					variant="subtle"
					colorScheme="accent"
					marginTop="$5"
					marginBottom="$5"
				>
					Report Issue
				</Button>
				<Switch>
					<Match when={reportSuccess() === false}>
						<Alert status="danger" variant="left-accent">
							<AlertIcon mr="$2_5" />
							<Flex>
								<AlertTitle marginRight="$1">Something went wrong!</AlertTitle>
								<AlertDescription>
									Failed to upload your report. Please try again later.
								</AlertDescription>
							</Flex>
						</Alert>
					</Match>
					<Match when={reportSuccess()}>
						<Alert status="success" variant="left-accent">
							<AlertIcon mr="$2_5" />
							<Flex>
								<AlertTitle marginRight="$1">Reported!</AlertTitle>
								<AlertDescription>
									You can track your issue{" "}
									<Anchor href={userCommentUrl()} color="$info9" external>
										here
									</Anchor>
								</AlertDescription>
							</Flex>
						</Alert>
					</Match>
				</Switch>
			</Box>
		</Box>
	);
}
