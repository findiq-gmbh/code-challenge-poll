<script lang="ts">
	import { onMount } from 'svelte';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	let questions: Question[] = [];
	let loading = true;
	let error = '';
	let text = '';
	let message = '';

	async function handleSubmit() {
		message = '';
		try {
			const response = await fetch(`${PUBLIC_BACKEND_URL}/question`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ text })
			});
			if (response.ok) {
				message = 'Question submitted successfully!';
				text = '';
			} else {
				message = 'Failed to submit question.';
			}
		} catch (error) {
			message = 'Error submitting question.';
		}
	}

	async function fetchQuestions() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${PUBLIC_BACKEND_URL}/question`);
			if (res.ok) {
				questions = await res.json();
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

	//Refresh questions after submitting a new one
	$: if (message === 'Question submitted successfully!') {
		fetchQuestions();
	}
</script>

<form class="form-wrapper" on:submit|preventDefault={handleSubmit}>
	<input id="question" type="text" placeholder="Write your question" bind:value={text} required />
	<button class="submit-button" type="submit">Submit</button>
</form>

{#if message}
	<p>{message}</p>
{/if}

{#if loading}
	<p>Loading questions...</p>
{:else if error}
	<p>{error}</p>
{:else if questions.length > 0}
	<h2 class="title">All Questions</h2>
	<ul class="questions">
		{#each questions as question (question.id)}
			<li class="question-wrapper">
				<h3>{question.text}</h3>
				<a class="answers-link" href="/answers/{question.id}">Show Answers</a>
			</li>
		{/each}
	</ul>
{:else}
	<p>No Questions Yet!</p>
{/if}

<style>
	.title {
		font-size: 20px;
		font-weight: bold;
	}
	.form-wrapper {
		display: flex;
		margin: 10px 0;
		padding: 8px;
		border-radius: 20px;
		justify-content: center;
		gap: 8px;
		background: #ff5925;
		width: 100%;
		box-sizing: border-box;
	}

	#question {
		background: #fff;
		width: 100%;
		border: 0;
		border-radius: 10px;
		padding: 12px;
		font-size: 18px;
	}
	.submit-button {
		width: 80px;
		margin: 4px 4px 4px -92px;
		border: none;
		border-radius: 8px;
		background: #ff5925;
		color: #fff;
		text-transform: uppercase;
	}
	.questions {
		list-style: none;
		padding: 0;
	}
	.question-wrapper {
		width: 100%;
		padding: 20px;
		border-radius: 10px;
		background-color: #fff;
		margin: 10px 0;
		display: flex;
		flex-direction: column;
		box-sizing: border-box;
	}
	.answers-link {
		margin-left: auto;
		display: inline-block;
		padding: 10px;
		border-radius: 10px;
		background-color: #ff3e00;
		color: #fff;
	}
</style>
