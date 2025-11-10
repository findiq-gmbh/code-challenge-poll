<script lang="ts">
	import { onMount } from 'svelte';

	let answers: Answer[] = [];
	let loading = true;
	let error = '';
	let text = '';
	let message = '';

	async function fetchAnswers() {
		loading = true;
		error = '';
		try {
			const response = await fetch('/api/answer/');
			if (response.ok) {
				answers = await response.json();
			} else {
				error = 'Failed to load questions.';
			}
		} catch (e) {
			error = 'Error loading questions.';
		} finally {
			loading = false;
		}
	}

	onMount(fetchAnswers);
</script>

<h2>Answers Overview</h2>

{#if loading}
	<p>Loading answers...</p>
{:else if error}
	<p>{error}</p>
{:else if answers.length === 0}
	<p>No answers yet.</p>
{:else}
	<table>
		<thead>
			<tr>
				<th style="text-align:left">Answer</th>
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
