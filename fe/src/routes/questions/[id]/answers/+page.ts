import type { AnswersWithQuestion } from '../../../models';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
	const { id } = params;

	try {
		const res = await fetch(`http://localhost:8000/question/${id}/answers`);
		if (!res.ok) {
			throw new Error('Failed to load answers');
		}
		const response: AnswersWithQuestion = await res.json();
		return { id, response };
	} catch (error) {
		return { id, error };
	}
};
