import { PUBLIC_API_URL } from '$env/static/public';
import type { PageLoad } from './$types';

export interface QuestionWithVisits {
	id: number;
	text: string;
	visit_count: number;
}

export const load: PageLoad = async ({ fetch }) => {
	const res = await fetch(`${PUBLIC_API_URL}/visits/`);
	const questions: QuestionWithVisits[] = res.ok ? await res.json() : [];
	return { questions };
};
