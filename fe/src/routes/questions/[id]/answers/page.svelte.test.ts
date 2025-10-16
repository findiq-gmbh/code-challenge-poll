// Import the necessary utilities from Vitest and vitest-browser-svelte
import { describe, it, expect } from 'vitest';
import { render } from 'vitest-browser-svelte';
import { page } from '@vitest/browser/context';
import Page from './+page.svelte';

const mockData = {
	id: '1',
	response: {
		question_text: 'How to learn CSS fast?',
		answers: [
			{ id: 1, text: 'First answer', question_id: 1 },
			{ id: 2, text: 'Second answer', question_id: 1 }
		]
	}
};

const mockDataWithError = {
	id: '1',
	error: 'Failed to fetch questions'
};

describe('+page.svelte', () => {
	it('renders question data with correct views', async () => {
		render(Page, { data: mockData });

		const heading = page.getByRole('heading', { level: 1, name: 'How to learn CSS fast?' });
		await expect.element(heading).toBeInTheDocument();

		const questionItem = page.getByText('First answer');
		await expect.element(questionItem).toBeInTheDocument;
	});
	it('renders error when data is not fetched', async () => {
		render(Page, { data: mockDataWithError });
		const error = page.getByText('Failed to fetch questions');
		await expect.element(error).toBeInTheDocument;
	});
});
