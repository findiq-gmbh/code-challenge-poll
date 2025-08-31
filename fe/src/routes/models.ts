export interface Question {
	id: number;
	text: string;
	answer_view_count: number;
}

export interface Answer {
	id: number;
	text: string;
	question_id: number;
}
