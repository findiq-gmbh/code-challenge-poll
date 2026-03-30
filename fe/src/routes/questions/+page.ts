import { PUBLIC_API_URL } from '$env/static/public';
import type { PageLoad } from './$types';
import type { Question } from '../models';

export const load: PageLoad = async ({ fetch }) => {
	const res = await fetch(`${PUBLIC_API_URL}/questions/`);
	const questions: Question[] = res.ok ? await res.json() : [];
	return { questions };
};
