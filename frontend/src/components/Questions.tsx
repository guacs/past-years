import { Box } from "@hope-ui/solid";
import { useNavigate, useParams } from "@solidjs/router";
import {
	For,
	Match,
	Resource,
	Switch,
	createEffect,
	createMemo,
	createSignal,
} from "solid-js";

import { Question } from "../types";
import FetchError from "./FetchError";
import Pagination from "./Pagination";
import FullQuestion from "./SingleQuestion";
import LoadingQuestion from "./questions/LoadingQuestion";

// ----- Constants -----
const QUESTIONS_PER_PAGE = 10 as const;

// ----- Props Interfaces/Types -----
interface QuestionsProps {
	questions: Resource<Question[]>;
}

export default function Questions(props: QuestionsProps) {
	const [numOfQuestions, setNumOfQuestions] = createSignal<number>(0);
	// const [currPageNum, setCurrPageNum] = createSignal<number>(0);

	const params = useParams();
	const navigate = useNavigate();

	createEffect(() => {
		const _questions = props.questions();
		if (_questions) {
			setNumOfQuestions(_questions.length);
		}
	});

	function getNumberOfPages() {
		return Math.ceil(numOfQuestions() / QUESTIONS_PER_PAGE);
	}

	function onPageChange(newPageNum: number) {
		// This is needed, because `navigate` removes all the query parameters.
		const searchParams = new URLSearchParams(window.location.search);
		navigate(`/questions/${newPageNum + 1}?${searchParams.toString()}`, {
			resolve: false,
		});
	}

	const startPageNum = createMemo(() => {
		const currPageNum = getCurrPage();
		return currPageNum * QUESTIONS_PER_PAGE;
	});

	/** Returns the current page number (1st page = 0) */
	function getCurrPage() {
		const currPageNum = Number(params.pageNum);
		return Number.isNaN(currPageNum) ? 0 : currPageNum - 1;
	}

	return (
		<Box>
			<Switch>
				<Match when={props.questions.loading}>
					<Box margin="$10" padding="$10">
						<LoadingQuestions />
					</Box>
				</Match>
				<Match when={props.questions.error}>
					<FetchError error={props.questions.error} />
				</Match>
				<Match when={props.questions()}>
					<For
						each={props
							.questions()
							?.slice(startPageNum(), startPageNum() + QUESTIONS_PER_PAGE)}
					>
						{(question, idx) => {
							const bgColor = idx() % 2 ? "$neutral2" : "$loContrast";
							return (
								<Box bgColor={bgColor}>
									<FullQuestion
										question={question}
										num={idx() + 1 + startPageNum()}
										showMetadata
										bgColor={bgColor}
									/>
								</Box>
							);
						}}
					</For>
					<Pagination
						numOfPages={getNumberOfPages()}
						numOfButtons={5}
						onPageClick={onPageChange}
						startingPage={getCurrPage()}
					/>
				</Match>
			</Switch>
		</Box>
	);
}

function LoadingQuestions() {
	return <For each={Array.from(Array(5))}>{() => <LoadingQuestion />}</For>;
}
