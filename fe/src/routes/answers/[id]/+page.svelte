<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import type { Answer, Question } from '@/routes/models';
	import { API_BASE_URL } from '@/config';

	const id = page.params.id;
	let answers: Answer[] = [];
	let question: Question | null = null;
	let loading = true;
	let error = '';
	let text = '';
	let message = '';

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		try {
			const response = await fetch(`${API_BASE_URL}/questions/${id}/answers`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ text, question_id: id })
			});
			if (response.ok) {
				message = 'Answer submitted successfully!';
				text = '';
			} else {
				message = 'Failed to submit answer.';
			}
		} catch (error) {
			message = 'Error submitting answer.';
		}
	}

	async function fetchAnswers() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${API_BASE_URL}/questions/${id}/answers?offset=0&limit=10`);
			if (res.ok) {
				answers = await res.json();
			} else {
				error = 'Failed to load answer.';
			}
		} catch (e) {
			error = 'Error loading answer.';
		} finally {
			loading = false;
		}
	}

	async function fetchQuestion() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`http://localhost:8000/questions/${id}`);
			if (res.ok) {
				question = await res.json();
			} else {
				error = 'Failed to load question.';
			}
		} catch (e) {
			error = 'Error loading question.';
		} finally {
			loading = false;
		}
	}
	onMount(() => {
		fetchAnswers();
		fetchQuestion();
	});

	$: if (message === 'Answer submitted successfully!') {
		fetchAnswers();
	}
</script>

<h1>{question?.title}</h1>
<form on:submit|preventDefault={handleSubmit}>
	<label for="answer">Answer:</label>
	<input id="answer" type="text" bind:value={text} required />
	<button type="submit">Submit</button>
</form>

{#if loading}
	<p>Loading...</p>
{:else if error}
	<p>{error}</p>
{:else}
	<ul>
		{#each answers as ans (ans.id)}
			<li>{ans.text}</li>
		{/each}
	</ul>
{/if}
