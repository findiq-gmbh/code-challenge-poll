<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import FormInput from '$lib/components/FormInput.svelte';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import Container from '$lib/components/Container.svelte';

	export let data: PageData;

	async function handleAnswerSubmit(text: string) {
		const res = await fetch('http://localhost:8000/answers', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ question_id: data.id, text })
		});
		if (!res.ok) {
			throw new Error('Failed to submit question');
		}
		await invalidateAll();
	}

	async function trackPageView() {
		try {
			const res = await fetch(`http://localhost:8000/questions/${data.id}/views`, {
				method: 'PATCH',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ question_id: data.id })
			});

			if (!res.ok) {
				console.error('Failed to track page view', res.statusText);
			}
		} catch (err) {
			console.error('Network error tracking page view', err);
		}
	}

	onMount(() => {
		if (!data.error) {
			trackPageView();
		}
	});
</script>

<Container>
	<h1>{data.response?.question_text}</h1>

	<FormInput placeholder="Write an answer..." buttonLabel="Submit" onSubmit={handleAnswerSubmit} />

	{#if data.error}
		<p class="error">{data.error}</p>
	{:else}
		<p>Answers</p>
		<ul class="list">
			{#each data.response?.answers as answer (answer.id)}
				<li class="list-item">
					<span class="text">{answer.text}</span>
				</li>
			{/each}
		</ul>
	{/if}
</Container>

<style>
	.list {
		list-style: none;
		padding: 0;
		margin: 0;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.list-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem;
		border: 1px solid #ddd;
		border-radius: 6px;
		background: #fafafa;
		transition: background-color 0.2s;
	}

	.list-item:hover {
		background: #f0f0f0;
	}

	.text {
		width: 80%;
	}
</style>
