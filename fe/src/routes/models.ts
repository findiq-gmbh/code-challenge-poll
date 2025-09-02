export interface Question {
	id: number;
	title: string;
	visitor_count: number;
}

export interface Answer {
	id: number;
	text: string;
	question_id: number;
}
