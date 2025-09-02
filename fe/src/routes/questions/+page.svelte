<script lang="ts">
	import { onMount } from 'svelte';
	import type { Question } from '@/routes/models';
	import { API_BASE_URL } from '@/config';
	let questions: Question[] = [];
	let loading = true;
	let error = '';
	let title = '';
	let message = '';

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		message = '';
		try {
			const response = await fetch(`${API_BASE_URL}/questions`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ title })
			});
			if (response.ok) {
				message = 'Question submitted successfully!';
				title = '';
			} else {
				message = 'Failed to submit question.';
			}
		} catch (error) {
			message = 'Error submitting question.';
		}
	}

	async function fetchQuestions() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${API_BASE_URL}/questions?offset=0&limit=10`);
			if (res.ok) {
				questions = await res.json();
			} else {
				error = 'Failed to load questions.';
			}
		} catch (e) {
			error = 'Error loading questions.';
		} finally {
			loading = false;
		}
	}

	onMount(fetchQuestions);

	//Refresh questions after submitting a new one
	$: if (message === 'Question submitted successfully!') {
		fetchQuestions();
	}
</script>

<form on:submit|preventDefault={handleSubmit}>
	<label for="question">Question:</label>
	<input id="question" type="text" bind:value={title} required />
	<button type="submit">Submit</button>
</form>

{#if message}
	<p>{message}</p>
{/if}

{#if loading}
	<p>Loading questions...</p>
{:else if error}
	<p>{error}</p>
{:else}
	<h2>All Questions</h2>
	<ul>
		{#each questions as question (question.id)}
			<li>{question.title}</li>
			<a href="/answers/{question.id}">Show Answers</a>
		{/each}
	</ul>
{/if}
