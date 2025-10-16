import { describe, it, expect } from 'vitest';
import { render } from 'vitest-browser-svelte';
import { page } from '@vitest/browser/context';
import Page from './+page.svelte';

const mockData = {
	questions: [
		{ id: 1, text: 'First question', views: 10 },
		{ id: 2, text: 'Second question', views: 0 }
	]
};

const mockDataWithError = {
	questions: [],
	error: 'Failed to fetch questions'
};

describe('+page.svelte', () => {
	it('renders question data with correct views', async () => {
		render(Page, { data: mockData });

		const heading = page.getByRole('heading', { level: 1, name: 'Questions Views' });
		await expect.element(heading).toBeInTheDocument();

		const questionItem = page.getByText('First question');
		await expect.element(questionItem).toBeInTheDocument;

		const secondQuestionItem = page.getByText('10 Views');
		await expect.element(secondQuestionItem).toBeInTheDocument;
	});
	it('renders error when data is not fetched', async () => {
		render(Page, { data: mockDataWithError });
		const error = page.getByText('Failed to fetch questions');
		await expect.element(error).toBeInTheDocument;
	});
});
