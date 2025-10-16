<script lang="ts">
	import Container from '$lib/components/Container.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<Container>
	{#if !data.questions.length}
		<p>No Questions to show</p>
	{:else}
		<h1>Questions Views</h1>

		{#if data.error}
			<p class="error">{data.error}</p>
		{:else}
			<ul class="list">
				{#each data.questions as question (question.id)}
					<li class="item">
						<span class="text">{question.text}</span>
						<span>{question.views} views</span>
					</li>
				{/each}
			</ul>
		{/if}
	{/if}
</Container>

<style>
	.list {
		list-style: none;
		padding: 0;
		margin: 0;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem;
		border: 1px solid #ddd;
		border-radius: 6px;
		background: #fafafa;
	}

	.text {
		width: 80%;
	}
</style>
