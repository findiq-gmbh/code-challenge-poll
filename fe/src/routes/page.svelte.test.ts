import { describe, expect, it } from 'vitest';
import { render } from 'vitest-browser-svelte';
import Page from './+page.svelte';

describe('/+page.svelte', () => {
	it('should set document title', () => {
		render(Page);

		expect(document.title).toBe('Home');
	});
});
