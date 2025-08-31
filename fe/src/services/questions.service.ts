const increaseQuestionAnswerViewCount = async (questionId: string): Promise<void> => {
	const response = await fetch(
		`http://localhost:8000/question/${questionId}/increase_answer_view_count`,
		{
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			}
		}
	);

	if (response.ok) {
		return response.json();
	} else {
		throw new Error('Failed to increase answer view count.');
	}
};

const readAllQuestions = async (): Promise<Question[]> => {
	const response = await fetch(`http://localhost:8000/questions`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		}
	});

	if (response.ok) {
		return response.json();
	} else {
		throw new Error('Failed to fetch questions.');
	}
};

export { increaseQuestionAnswerViewCount, readAllQuestions };
