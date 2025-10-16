<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import Container from '$lib/components/Container.svelte';
	import FormInput from '$lib/components/FormInput.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
	let questionCountText = '';

	async function handleQuestionSubmit(text: string) {
		const res = await fetch('http://localhost:8000/question', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ text })
		});
		if (!res.ok) {
			throw new Error('Failed to submit question');
		}
		await invalidateAll();
	}

	$: {
		const count = data.questions.length;
		if (count === 0) {
			questionCountText = 'No questions';
		} else if (count === 1) {
			questionCountText = '1 Question';
		} else {
			questionCountText = `${count} Questions`;
		}
	}
</script>

<Container>
	<h1>Questions</h1>

	<FormInput placeholder="Ask a question..." buttonLabel="Ask" onSubmit={handleQuestionSubmit} />

	{#if data.error}
		<p class="error">{data.error}</p>
	{:else}
		<p>{questionCountText}</p>
		<ul class="list">
			{#each data.questions as question (question.id)}
				<li class="item">
					<span class="text">{question.text}</span>
					<a href={`/questions/${question.id}/answers`}>Show Answers →</a>
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

	.item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem;
		border: 1px solid #ddd;
		border-radius: 6px;
		background: #fafafa;
		transition: background-color 0.2s;
	}

	.item:hover {
		background: #f0f0f0;
	}

	.item a {
		color: #007bff;
		text-decoration: none;
		font-size: 0.9rem;
	}

	.item a:hover {
		text-decoration: underline;
	}

	.text {
		width: 80%;
	}
</style>
