<script lang="ts">
	import { onMount } from 'svelte';

	type Visit = { question_id: number; text: string; visit_count: number };
	let visits: Visit[] = [];
	let loading = true;
	let error = '';

	async function fetchVisits() {
		loading = true;
		error = '';
		try {
			const response = await fetch('/api/visits');
			if (!response.ok) {
				throw new Error('Failed to load visits');
			}
			visits = await response.json();
			visits.sort((a, b) => b.visit_count - a.visit_count);
		} catch (e) {
			error = 'Error loading visits';
		} finally {
			loading = false;
		}
	}

	onMount(fetchVisits);
</script>

<h2>Visits Overview</h2>

{#if loading}
	<p>Loading visits...</p>
{:else if error}
	<p>{error}</p>
{:else if visits.length === 0}
	<p>No visits yet.</p>
{:else}
	<table>
		<thead>
			<tr>
				<th style="text-align:left">Question</th>
				<th style="text-align:right">Visits</th>
			</tr>
		</thead>
		<tbody>
			{#each visits as visit}
				<tr>
					<td style="text-align:left">{visit.text}</td>
					<td style="text-align:right">{visit.visit_count}</td>
				</tr>
			{/each}
		</tbody>
	</table>
{/if}
