<script lang="ts">
	import { onMount } from 'svelte';
	import { readAllQuestions } from '../../services/questions.service';
	let questions: Question[] = [];
	let isLoading = false;

	onMount(async () => {
		isLoading = true;
		questions = await readAllQuestions();
		isLoading = false;
	});
</script>

{#if isLoading}
	<div>Loading...</div>
{:else}
	<table>
		<thead>
			<tr>
				<th>Question</th>
				<th>Answer Count</th>
			</tr>
		</thead>
		<tbody>
			{#each questions as question (question.id)}
				<tr>
					<td>{question.text}</td>
					<td>{question.answer_view_count}</td>
				</tr>
			{/each}
		</tbody>
	</table>
{/if}
