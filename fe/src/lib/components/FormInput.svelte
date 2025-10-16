<script lang="ts">
	import { fade } from 'svelte/transition';

	export let placeholder: string;

	export let buttonLabel: string;

	export let onSubmit: (text: string) => Promise<void> | void;

	let text = '';
	let message = '';
	let error = '';
	let timeout: ReturnType<typeof setTimeout>;

	function showToast(text: string) {
		clearTimeout(timeout);
		message = text;
		timeout = setTimeout(() => {
			message = '';
		}, 5000);
	}

	async function handleSubmit() {
		message = '';

		try {
			await onSubmit(text);
			text = '';
			showToast('Submitted successfully!');
		} catch (err) {
			console.error(err);
			error = 'Error submitting.';
		}
	}

	$: canSubmit = text.trim().length > 0;
</script>

<form on:submit|preventDefault={handleSubmit} class="form">
	<textarea {placeholder} bind:value={text} required></textarea>
	<button disabled={!canSubmit} type="submit">{buttonLabel}</button>
</form>

{#if message}
	<p transition:fade class="message">{message}</p>
{/if}

{#if error}
	<p class="error">{error}</p>
{/if}

<style>
	.form {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		margin-bottom: 1rem;
		align-items: center;
	}

	@media (min-width: 500px) {
		.form {
			flex-direction: row;
		}
	}

	textarea {
		flex: 1;
		padding: 0.5rem 0.75rem;
		font-size: 1rem;
		border-radius: 6px;
		height: 4rem;
	}

	button {
		background-color: #007bff;
		color: white;
		padding: 0.5rem 1rem;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		transition: background-color 0.2s ease;
		height: 2rem;
	}

	button:disabled {
		cursor: not-allowed;
		background-color: gray;
	}

	button:hover:not(:disabled) {
		background-color: #0056b3;
	}

	.message {
		text-align: center;
		font-weight: 500;
		margin-top: 0.5rem;
	}

	.error {
		text-align: center;
		font-weight: 500;
		margin-top: 0.5rem;
		background-color: red;
	}
</style>
