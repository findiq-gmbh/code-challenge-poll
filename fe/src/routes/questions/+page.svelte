<script lang="ts">
	import { onMount } from 'svelte';

	let questions: Question[] = [];
	let loading = true;
	let error = '';
	let text = '';
	let message = '';
	let submitting = false;

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		if (submitting) {
			return;
		}
		message = '';

		try {
			submitting = true;
			const response = await fetch('/api/question/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ text })
			});
			if (response.ok) {
				message = 'Question submitted successfully!';
				text = '';
				fetchQuestions();
			} else {
				message = 'Failed to submit question.';
			}
		} catch (error) {
			message = 'Error submitting question.';
		} finally {
			submitting = false;
		}
	}

	async function fetchQuestions() {
		loading = true;
		error = '';
		try {
			const response = await fetch('/api/question/');
			if (response.ok) {
				questions = await response.json();
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
</script>

<div class="form-content">
	<form on:submit|preventDefault={handleSubmit}>
		<label for="question">Question:</label>
		<input id="question" type="text" bind:value={text} required />
		<button type="submit" disabled={submitting}>{submitting ? 'Submitting...' : 'Submit'}</button>
	</form>

	{#if message}
		<p>{message}</p>
	{/if}
</div>

{#if loading}
	<p>Loading questions...</p>
{:else if error}
	<p>{error}</p>
{:else if questions.length === 0}
	<p>No questions yet.</p>
{:else}
	<table>
		<thead>
			<tr>
				<th style="text-align:left">Question</th>
				<th style="text-align:right"></th>
			</tr>
		</thead>
		<tbody>
			{#each questions as question}
				<tr>
					<td>{question.text}</td>
					<td style="text-align:center">
						<a href="/answers/{question.id}">Show Answers</a>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
{/if}
