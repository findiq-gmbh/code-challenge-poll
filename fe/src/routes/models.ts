interface Question {
	id: number;
	text: string;
	answer_view_count: number;
}

interface Answer {
	id: number;
	text: string;
	question_id: number;
}
