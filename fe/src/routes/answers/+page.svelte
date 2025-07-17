<script lang="ts">
	import { onMount } from 'svelte';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	let answers: Answer[] = [];
	let loading = true;
	let error = '';
	let message = '';

	async function fetchAnswers() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${PUBLIC_BACKEND_URL}/answer`);
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

	$: if (message === 'Answer submitted successfully!') {
		fetchAnswers();
	}
</script>

{#if loading}
	<p>Loading...</p>
{:else if error}
	<p>{error}</p>
{:else if answers.length > 0}
	<ul>
		{#each answers as ans (ans.id)}
			<li>{ans.text}</li>
		{/each}
	</ul>
{:else}
	<p>No Answers Yet!</p>
{/if}
