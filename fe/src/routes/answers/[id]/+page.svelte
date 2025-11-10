<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';

	const id = get(page).params.id;
	let answers: Answer[] = [];
	let loading = true;
	let error = '';
	let text = '';
	let message = '';
	let submitting = false;

	async function trackVisit() {
		try {
			await fetch(`/api/question/${id}/visit`, { method: 'POST' });
		} catch (e) {
			console.warn('Visit tracking failed', e);
		}
	}

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		if (submitting) {
			return;
		}
		message = '';

		try {
			const response = await fetch('/api/answer/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ text, question_id: id })
			});
			if (response.ok) {
				message = 'Answer submitted successfully!';
				text = '';
				fetchAnswers();
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
			const response = await fetch('/api/answer/');
			if (response.ok) {
				const answer: Answer[] = await response.json();
				answers = answer.filter((ans) => ans.question_id === parseInt(id));
			} else {
				error = 'Failed to load answer.';
			}
		} catch (e) {
			error = 'Error loading answer.';
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		trackVisit();
		fetchAnswers();
	});
</script>

<div class="form-content">
	<form on:submit|preventDefault={handleSubmit}>
		<label for="answer">Answer:</label>
		<input id="answer" type="text" bind:value={text} required />
		<button type="submit" disabled={submitting}>{submitting ? 'Submitting...' : 'Submit'}</button>
	</form>

	{#if message}
		<p>{message}</p>
	{/if}
</div>

{#if loading}
	<p>Loading answers...</p>
{:else if error}
	<p>{error}</p>
{:else if answers.length === 0}
	<p>No answers yet for this question.</p>
{:else}
	<table>
		<thead>
			<tr>
				<th style="text-align:left">Answers</th>
				<th style="text-align:right">Question ID</th>
			</tr>
		</thead>
		<tbody>
			{#each answers as answer}
				<tr>
					<td style="text-align:left">{answer.text}</td>
					<td style="text-align:right">{answer.question_id}</td>
				</tr>
			{/each}
		</tbody>
	</table>
{/if}
