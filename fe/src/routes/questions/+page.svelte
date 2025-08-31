<script lang="ts">
	import { onMount } from 'svelte';
	let questions: Question[] = [];
	let loading = true;
	let error = '';
	let text = '';
	let message = '';

	// Feedback: `message` is used for two purposes: displaying feedback and errors. Consider using global `error` variable.
	//           You might want to show `errors` and `messages` in a different visualisation.
	async function handleSubmit(event: SubmitEvent) {
		// Feedback: Is this `preventDefault` necessary due to the `preventDefault` on the `<form/>` element?
		event.preventDefault();
		message = '';
		try {
			// Feedback: The API is paginated and only allows a max of 100 questions in return.
			//           Consider implementing pagination in the frontend to handle this.
			const response = await fetch('http://localhost:8000/question', {
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
			// Feedback: `error` from `catch()` is unused, you can remove it.
			message = 'Error submitting question.';
		}
	}

	async function fetchQuestions() {
		loading = true;
		error = '';
		try {
			const res = await fetch('http://localhost:8000/question');
			if (res.ok) {
				questions = await res.json();
			} else {
				error = 'Failed to load questions.';
			}
		} catch (e) {
			// Feedback: `e` from `catch()` is unused, you can remove it.
			error = 'Error loading questions.';
		} finally {
			loading = false;
		}
	}

	onMount(fetchQuestions);

	// Feedback: Listening on `message` value for logic decisions, can lead to unexpected behavior if `message` changes unexpectedly
	// Suggestion: Use a variable that indicates that the server's data might have changed, so that a reload is necessary
	//Refresh questions after submitting a new one
	$: if (message === 'Question submitted successfully!') {
		fetchQuestions();
	}
</script>

<!-- Feedback: I am not a svelt expert knowing what this `preventDefault` is doing, but in the handler you are preventing the default behavior of the form submission -->
<form on:submit|preventDefault={handleSubmit}>
	<label for="question">Question:</label>
	<input id="question" type="text" bind:value={text} required />
	<button type="submit">Submit</button>
</form>

{#if message}
	<p>{message}</p>
{/if}

{#if loading}
	<p>Loading questions...</p>
{:else if error}
	<p>{error}</p>
{:else}
	<h2>All Questions</h2>
	<ul>
		<!-- Feedback: Svelte requires each block having a key in a loop -->
		{#each questions as question}
			<li>{question.text}</li>
			<a href="/answers/{question.id}">Show Answers</a>
		{/each}
	</ul>
{/if}
