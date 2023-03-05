import globalAxios from "axios";
import camelcaseKeys from "camelcase-keys";
import { Question, QuestionsMetadata } from "./types";
import { title } from "./utils";

// ----- Axios Configurations ------
const axios = globalAxios.create({
	headers: {
		Accept: "application/json",
	},
	baseURL: "http://localhost:8080",
});

// ----- Endpoints -----
const QUESTIONS = "/questions" as const;
const FILTERED_QUESTIONS = `${QUESTIONS}/filter` as const;
const RANDOM = "/questions/random" as const;
const QUESTIONS_METADATA = "/questions/metadata" as const;
const INCORRECT_QUESTION = "/incorrect-question/" as const;

// ----- API Calls -----
/** Fetches the questions. */
async function fetchQuestions(endpoint: string) {
	const response = await axios.get<Question[]>(endpoint);
	return camelcaseKeys(response.data);
}

/** Fetches the questions based on the given filter. */
export async function fetchFilteredQuestions(
	filter: string,
): Promise<Question[]> {
	const endpoint =
		filter.length === 0
			? FILTERED_QUESTIONS
			: `${FILTERED_QUESTIONS}?${filter}`;
	return await fetchQuestions(endpoint);
}

/** Fetches a random set of 100 questions based on the given filter. */
export async function fetchRandomQuestions(
	filter: string,
): Promise<Question[]> {
	const endpoint = filter.length === 0 ? RANDOM : `${RANDOM}?${filter}`;
	return await fetchQuestions(endpoint);
}

export async function fetchQuestionsMetadata(): Promise<QuestionsMetadata> {
	const response = await axios.get<QuestionsMetadata>(QUESTIONS_METADATA);

	const metadata = response.data;
	metadata.subjects = metadata.subjects.map((s) => title(s));
	// The API actually returns a list of integers for the years.
	metadata.years = metadata.years.map((y) => y.toString());

	return metadata;
}

/** Fetches a single question. */
export async function fetchQuestion(id: string): Promise<Question> {
	const endpoint = `${QUESTIONS}/${id}`;
	const response = await axios.get<Question>(endpoint);
	console.log(response.data);
	return camelcaseKeys(response.data);
}

export async function fetchIncorrectQuestionUrl(id: string): Promise<string> {
	const endpoint = INCORRECT_QUESTION + id;
	const response = await axios.get<string>(endpoint);
	return response.data;
}

export async function reportIncorrectQuestion(
	question_id: string,
	comments: string,
): Promise<string> {
	const endpoint = INCORRECT_QUESTION + question_id;
	const response = await axios.post<string>(endpoint, {
		comments: comments,
	});
	return response.data;
}
