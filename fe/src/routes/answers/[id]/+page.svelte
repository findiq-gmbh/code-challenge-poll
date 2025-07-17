<script lang="ts">
	import { onMount } from 'svelte';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';
	const id = get(page).params.id;
	let answer: Answer[] = [];
	let qustionText: string = '';
	let loading = true;
	let error = '';
	let text = '';
	let message = '';

	async function handleSubmit() {
		// event.preventDefault();
		try {
			const response = await fetch(`${PUBLIC_BACKEND_URL}/answer`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ text, question_id: id })
			});
			if (response.ok) {
				message = 'Answer submitted successfully!';
				text = '';
			} else {
				message = 'Failed to submit answer.';
			}
		} catch (error) {
			message = 'Error submitting answer.';
		}
	}

	async function fetchAnswers() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${PUBLIC_BACKEND_URL}/answer`);
			if (res.ok) {
				const answers: Answer[] = await res.json();
				answer = answers.filter((ans) => ans.question_id === parseInt(id));
			} else {
				error = 'Failed to load answer.';
			}
		} catch (e) {
			error = 'Error loading answer.';
		} finally {
			loading = false;
		}
	}
	async function fetchQuestion() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${PUBLIC_BACKEND_URL}/question/${id}`);
			if (res.ok) {
				const question = await res.json();
				qustionText = question.text;
			} else {
				error = 'Failed to load question.';
			}
		} catch (e) {
			error = 'Error loading question.';
		} finally {
			loading = false;
		}
	}

	async function updateVisits() {
		try {
			await fetch(`${PUBLIC_BACKEND_URL}/visits/${id}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ answer_id: id })
			});
		} catch (error) {
			message = 'Error submitting answer.';
		}
	}

	onMount(async () => {
		await fetchQuestion();
		await fetchAnswers();
		await updateVisits();
	});

	$: if (message === 'Answer submitted successfully!') {
		fetchAnswers();
	}
</script>

<h3>{qustionText}</h3>

{#if loading}
	<p>Loading...</p>
{:else if error}
	<p>{error}</p>
{:else if answer.length > 0}
	<ul class="answers">
		{#each answer as ans (ans.id)}
			<li class="answer-wrapper">{ans.text}</li>
		{/each}
	</ul>
{:else}
	<p>No Answers Yet!</p>
{/if}

<form class="form-wrapper" on:submit|preventDefault={handleSubmit}>
	<input id="answer" placeholder="Write your answer" type="text" bind:value={text} required />
	<button class="submit-button" type="submit">Submit</button>
</form>

<style>
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
	#answer {
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

	.answers {
		padding: 0;
		list-style: inside;
	}
	.answer-wrapper {
		width: 100%;
		padding: 10px;
		border-radius: 10px;
		background-color: #fff;
		margin: 10px 0;
		box-sizing: border-box;
	}
</style>
