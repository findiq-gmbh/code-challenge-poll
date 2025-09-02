<script lang="ts">
	import { onMount } from 'svelte';
	import type { Answer } from '@/routes/models';
	import { API_BASE_URL } from '@/config';

	let answers: Answer[] = [];
	let loading = true;
	let error = '';

	async function fetchAnswers() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${API_BASE_URL}/answers?offset=0&limit=10`);
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

	onMount(() => {
		fetchAnswers();
	});
</script>

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
