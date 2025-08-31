<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';
	import { increaseQuestionAnswerViewCount } from '../../../services/questions.service';
	const id = get(page).params.id;
	// Feedback: Since the variable `answer` holds a list of answers, consider naming it `answers`
	let answer: Answer[] = [];
	let loading = true;
	let error = '';
	let text = '';
	let message = '';

	// Feedback: Indentation is incorrect.
	// Feedback: Submit could also use a loading indicator potentially
	// Feedback: Maybe reset `message` to an empty string, right now there will be always a message writing in the function, but it could lead to unexpected behavior in the future.
	async function handleSubmit(event: SubmitEvent) {
		// Feedback: Is this `preventDefault` necessary due to the `preventDefault` on the `<form/>` element?
		event.preventDefault();
		message = '';
		try {
			// Feedback: Extract service logic into a separate function
			//           Use an environment variable to provide `host` from outside, necessary if you want to deploy it.
			const response = await fetch('http://localhost:8000/answer', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				// Feedback: You could use zod for validation of the model and use it to show errors to the user
				body: JSON.stringify({ text, question_id: id })
			});
			if (response.ok) {
				message = 'Answer submitted successfully!';
				text = '';
			} else {
				message = 'Failed to submit answer.';
			}
		} catch {
			// Feedback: If you are not using the `error` variable, you can remove it
			message = 'Error submitting answer.';
		}
	}

	async function fetchAnswers() {
		loading = true;
		error = '';
		try {
			// Feedback: Extract service logic into a separate function
			//           Use an environment variable to provide `host` from outside, necessary if you want to deploy it.
			const res = await fetch('http://localhost:8000/answer');
			if (res.ok) {
				const answers: Answer[] = await res.json();
				// Feedback: This filter is needed since the API fetching logic does not provide a functionality to fetch answers by question_id.
				//           This is also not working, since the API does not allow fetching all answers, if there are more than 100 answers, you might not find answers for this question.
				// Suggestion: Extend the API to fetch answers by question_id, by either an additional endpoint or extending the existing one.
				//             My personal preference is to add a new endpoint `/question/:id/answers`, since it's a specific use case.
				answer = answers.filter((ans) => ans.question_id === parseInt(id));
			} else {
				error = 'Failed to load answer.';
			}
		} catch {
			// Feedback: Error variable from `catch` has same variable name as global `error`, and conflicts
			// Suggestion: If you don't need the `catch(error)` variable, you can remove it
			error = 'Error loading answer.';
		} finally {
			loading = false;
		}
	}
	onMount(() => {
		fetchAnswers();
		increaseQuestionAnswerViewCount(id);
	});

	// Feedback: Listening on `message` value for logic decisions, can lead to unexpected behavior if `message` changes unexpectedly
	// Suggestion: Use a variable that indicates that the server's data might have changed, so that a reload is necessary
	$: if (message === 'Answer submitted successfully!') {
		fetchAnswers();
	}
</script>

<!-- Feedback: I am not a svelt expert knowing what this `preventDefault` is doing, but in the handler you are preventing the default behavior of the form submission -->
<form on:submit|preventDefault={handleSubmit}>
	<label for="answer">Answer:</label>
	<input id="answer" type="text" bind:value={text} required />
	<button type="submit">Submit</button>
</form>

{#if loading}
	<p>Loading...</p>
{:else if error}
	<p>{error}</p>
{:else}
	<ul>
		<!-- Feedback: Svelte requires each block having a key in a loop -->
		{#each answer as ans (ans.id)}
			<li>{ans.text}</li>
		{/each}
	</ul>
{/if}
