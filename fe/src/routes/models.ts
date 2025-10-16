export interface Question {
	id: number;
	text: string;
	views: number;
}

export interface Answer {
	id: number;
	text: string;
	question_id: number;
}
export interface AnswersWithQuestion {
	question_text: string;
	answers: Answer[];
}
