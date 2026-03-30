import { error } from '@sveltejs/kit';
import { PUBLIC_API_URL } from '$env/static/public';
import type { PageLoad } from './$types';
import type { Answer, Question } from '../../models';

export const load: PageLoad = async ({ fetch, params }) => {
	const id = parseInt(params.id, 10);
	if (isNaN(id)) error(404, 'Not found');

	const [questionRes, answersRes] = await Promise.all([
		fetch(`${PUBLIC_API_URL}/questions/${id}`),
		fetch(`${PUBLIC_API_URL}/questions/${id}/answers`),
		fetch(`${PUBLIC_API_URL}/questions/${id}/visit`, { method: 'POST' })
	]);

	const question: Question | null = questionRes.ok ? await questionRes.json() : null;
	const answers: Answer[] = answersRes.ok ? await answersRes.json() : [];

	return { question, answers };
};
