import { Answers, Question } from "../../types";

export interface AnswerProps {
	answers: Answers;
	correctAnswer: string;
}

export interface QuestionProps {
	question: Question;
}

/** The props to the SingleQuestion component. */
export interface FullQuestionProps extends QuestionProps {
	num: number; // The question number
	showMetadata?: boolean;
	bgColor: string;
}
