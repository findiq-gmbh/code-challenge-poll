import type { PageLoad } from '../$types';
import type { Question } from '../../models';

export const load: PageLoad = async ({ fetch }) => {
	try {
		const res = await fetch('http://localhost:8000/question');
		if (!res.ok) {
			throw new Error('Failed to load questions');
		}
		const questions: Question[] = await res.json();
		return { questions };
	} catch (error) {
		return { questions: [] as Question[], error };
	}
};
