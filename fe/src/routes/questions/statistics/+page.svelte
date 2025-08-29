<script lang="ts">
	import { onMount } from 'svelte';
	
	const API_BASE_URL = 'http://localhost:8000';
	
	interface VisitStatistic {
		question_id: number;
		question_text: string;
		visit_count: number;
	}
	
	let statistics: VisitStatistic[] = [];
	let loading = true;
	let error = '';
	
	async function fetchStatistics() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${API_BASE_URL}/questions/visits`);
			if (res.ok) {
				statistics = await res.json();
			} else {
				error = 'Failed to load question visits.';
			}
		} catch (e) {
			error = 'Error loading statistics. Please check your connection.';
		} finally {
			loading = false;
		}
	}
	
	onMount(fetchStatistics);
</script>

<svelte:head>
	<title>Statistics</title>
	<meta name="description" content="Question visits" />
</svelte:head>

<div class="statistics-container">
	<h1>Visits Statistics</h1>
	
	{#if loading}
		<div class="loading">
			<p>Loading statistics...</p>
		</div>
	{:else if error}
		<div class="error">
			<p>{error}</p>
			<button on:click={fetchStatistics}>Retry</button>
		</div>
	{:else if statistics.length === 0}
		<div class="empty-state">
			<p>No visit data available yet.</p>
		</div>
	{:else}
		<div class="stats-table">
			<div class="table-header">
				<div class="id-col">ID</div>
				<div class="question-col">Question</div>
				<div class="visits-col">Visits</div>
				<div class="action-col">Action</div>
			</div>
			
			{#each statistics as stat}
				<div class="table-row">
					<div class="id-col">
						{stat.question_id}
					</div>
					<div class="question-col">
						<span class="question-text">{stat.question_text}</span>
					</div>
					<div class="visits-col">
						<span class="visit-count">{stat.visit_count}</span>
						<span class="visit-label">visits</span>
					</div>
					<div class="action-col">
						<a href="/questions/{stat.question_id}/answers" class="view-link">
							View Answers
						</a>
					</div>
				</div>
			{/each}
		</div>
		
		<div class="summary">
			<p>
				Total questions: <strong>{statistics.length}</strong> |
				Total visits: <strong>{statistics.reduce((sum, stat) => sum + stat.visit_count, 0)}</strong>
			</p>
		</div>
	{/if}
</div>

<style>
	.statistics-container {
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem 1rem;
	}
	
	h1 {
		text-align: center;
		margin-bottom: 2rem;
		color: #333;
	}
	
	.loading, .error, .empty-state {
		text-align: center;
		padding: 2rem;
		margin: 2rem 0;
	}
	
	.error {
		background-color: #fee;
		border: 1px solid #fcc;
		border-radius: 8px;
		color: #c33;
	}
	
	.error button {
		margin-top: 1rem;
		padding: 0.5rem 1rem;
		background-color: #c33;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}
	
	.empty-state {
		background-color: #f8f9fa;
		border: 1px solid #e9ecef;
		border-radius: 8px;
		color: #6c757d;
	}
	
	.stats-table {
		background: white;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0,0,0,0.1);
		overflow: hidden;
	}
	
	.table-header {
		display: grid;
		grid-template-columns: 60px 1fr 100px 120px;
		gap: 1rem;
		padding: 1rem;
		background-color: #f8f9fa;
		border-bottom: 2px solid #e9ecef;
		font-weight: bold;
		color: #495057;
		font-size: 0.9rem;
		text-transform: uppercase;
		letter-spacing: 0.5px;
	}
	
	.table-row {
		display: grid;
		grid-template-columns: 60px 1fr 100px 120px;
		gap: 1rem;
		padding: 1rem;
		border-bottom: 1px solid #e9ecef;
		align-items: center;
		transition: background-color 0.2s ease;
	}
	
	.rank-col {
		text-align: center;
		font-size: 1.2rem;
		font-weight: bold;
	}
	
	.question-col {
		min-width: 0;
	}
	
	.question-text {
		display: block;
		font-weight: 500;
		color: #333;
		word-wrap: break-word;
		line-height: 1.4;
	}
	
	.visits-col {
		text-align: center;
	}
	
	.visit-count {
		display: block;
		font-size: 1.5rem;
		font-weight: bold;
		color: #007bff;
	}
	
	.visit-label {
		font-size: 0.8rem;
		color: #6c757d;
		text-transform: uppercase;
	}
	
	.action-col {
		text-align: center;
	}
	
	.view-link {
		display: inline-block;
		padding: 0.4rem 0.8rem;
		background-color: #007bff;
		color: white;
		text-decoration: none;
		border-radius: 4px;
		font-size: 0.9rem;
		transition: background-color 0.2s ease;
	}
	
	.summary {
		margin-top: 2rem;
		padding: 1rem;
		background-color: #f8f9fa;
		border-radius: 8px;
		text-align: center;
		color: #495057;
	}
</style>
