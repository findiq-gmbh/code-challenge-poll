<script lang="ts">
	import { onMount } from 'svelte';
	import type { Question } from '@/routes/models';
	import { API_BASE_URL } from '@/config';

	let questions: Question[] = [];
	let loading = true;
	let error = '';

	async function fetchQuestions() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${API_BASE_URL}/questions?offset=0&limit=10`);
			if (res.ok) {
				questions = await res.json();
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
		fetchQuestions();
	});
</script>

{#if loading}
	<p>Loading...</p>
{:else if error}
	<p>{error}</p>
{:else}
	<table>
		<thead>
			<tr>
				<th>Title</th>
				<th>Visitor Count</th>
			</tr>
		</thead>
		<tbody>
			{#each questions as q (q.id)}
				<tr>
					<td>{q.title}</td>
					<td>{q.visitor_count}</td>
				</tr>
			{/each}
		</tbody>
	</table>
{/if}
