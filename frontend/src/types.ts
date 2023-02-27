/* The various interfaces/types used throughout the application. */

/** The interface for the answers in a single question. */
export interface Answers {
	a: string;
	b: string;
	c: string;
	d: string;
}

/** The interface for a single question. */
export interface Question {
	id: string;
	mainQuestion: string;
	continuation: string;
	questionOptions: string[];
	answers: Answers;
	correctAnswer: string;
	exam: string;
	subject: string;
	year: number;
}

/** The interface for the questions metadata. */
export interface QuestionsMetadata {
	exams: string[];
	years: string[];
	subjects: string[];
}
