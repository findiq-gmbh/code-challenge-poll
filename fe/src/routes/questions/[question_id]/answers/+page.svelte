<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';

	const API_BASE_URL = 'http://localhost:8000';
	const { question_id } = $page.params;
	
	let answers: Answer[] = [];
	let loading = true;
	let error = '';
	let text = '';
	let message = '';

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		message = '';

		const trimmedText = text.trim();
		if (!trimmedText) {
			message = 'Answer text cannot be empty';
			return;
		}

		try {
			const response = await fetch(`${API_BASE_URL}/answers/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ text, question_id: parseInt(question_id) })
			});
			if (response.ok) {
				message = 'Answer submitted successfully!';
				text = '';
			} else {
				const errorData = await response.json();
				message = `Failed to submit answer: ${errorData.detail}`;
			}
		} catch (error) {
			message = 'Error submitting answer.';
		}
	}

	async function trackVisit() {
		try {
			await fetch(`${API_BASE_URL}/question/${question_id}/visit`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				}
			});
		} catch (error) {
			message = 'Failed to track visit.';
		}
	}

	async function fetchAnswers() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${API_BASE_URL}/question/${question_id}/answers`);
			if (res.ok) {
				answers = await res.json();
			} else {
				error = 'Failed to load question and answers.';
			}
		} catch (e) {
			error = 'Error loading data. Please check your connection.';
		} finally {
			loading = false;
		}
	}
	onMount(() => {
		fetchAnswers();
		trackVisit();
	});

	$: if (message === 'Answer submitted successfully!') {
		fetchAnswers();
	}
</script>
<div>
	{#if loading}
		<div class="loading-state">
			<div class="spinner"></div>
			<p>Loading question and answers...</p>
		</div>
	{:else if error}
		<div class="error-state">
			<p>{error}</p>
			<a href="/questions" class="back-link">← Back to Questions</a>
		</div>
	{:else}
		<div class="form-section">
			<h2>Your Answer</h2>
			<form on:submit|preventDefault={handleSubmit} class="answer-form">
				<div class="input-group">
					<textarea 
						id="answer" 
						bind:value={text} 
						required 
						minlength="1"
						placeholder="Write your answer"
						class="answer-input"
						rows="3"
					></textarea>
					<button type="submit" class="submit-btn">Submit Answer</button>
				</div>
			</form>
			
			{#if message}
				<div class="message" class:success={message.includes('successfully')} class:error={!message.includes('successfully')}>
					{message}
				</div>
			{/if}
		</div>

		<div class="answers-section">
			<h2>All Answers ({answers.length})</h2>
			{#if answers.length === 0}
				<div class="empty-state">
					<p>No answers yet!</p>
				</div>
			{:else}
				<div class="answers-grid">
					{#each answers as answer, index}
						<div class="answer-card">
							<div class="answer-number"># {index + 1}</div>
							<div class="answer-text">{answer.text}</div>
						</div>
					{/each}
				</div>
			{/if}
		</div>
	{/if}
</div>


<style>	
	.loading-state {
		text-align: center;
		padding: 3rem;
		color: #6c757d;
	}
	
	.spinner {
		width: 40px;
		height: 40px;
		border: 4px solid #f3f3f3;
		border-top: 4px solid #007bff;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin: 0 auto 1rem;
	}
	
	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}
	
	.error-state {
		text-align: center;
		padding: 2rem;
		background-color: #f8d7da;
		color: #721c24;
		border-radius: 8px;
		border: 1px solid #f5c6cb;
	}
	
	.back-link {
		display: inline-block;
		margin-top: 1rem;
		padding: 0.5rem 1rem;
		background-color: #007bff;
		color: white;
		text-decoration: none;
		border-radius: 4px;
	}
	
	.form-section {
		background: white;
		border-radius: 12px;
		padding: 2rem;
		box-shadow: 0 4px 20px rgba(0,0,0,0.08);
		margin-bottom: 3rem;
		border: 1px solid #e9ecef;
	}
	
	.form-section h2 {
		margin-bottom: 1.5rem;
		color: #495057;
		font-size: 1.5rem;
	}
	
	.answer-form {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
	
	.input-group {
		display: flex;
		gap: 1rem;
		align-items: flex-end;
	}
	
	.answer-input {
		flex: 1;
		padding: 1rem;
		border: 2px solid #e9ecef;
		border-radius: 8px;
		font-size: 1rem;
		font-family: inherit;
		resize: vertical;
		min-height: 80px;
		transition: border-color 0.3s ease;
	}
	
	.answer-input:focus {
		outline: none;
		border-color: #007bff;
		box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
	}
	
	.answer-input:disabled {
		background-color: #f8f9fa;
		color: #6c757d;
	}
	
	.submit-btn {
		padding: 1rem 2rem;
		background-color: #28a745;
		color: white;
		border: none;
		border-radius: 8px;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.3s ease;
		white-space: nowrap;
		align-self: flex-start;
	}

	.submit-btn:disabled {
		background-color: #6c757d;
		cursor: not-allowed;
		transform: none;
	}
	
	.message {
		padding: 1rem;
		border-radius: 8px;
		margin-top: 1rem;
		font-weight: 500;
	}
	
	.message.success {
		background-color: #d4edda;
		color: #155724;
		border: 1px solid #c3e6cb;
	}
	
	.message.error {
		background-color: #f8d7da;
		color: #721c24;
		border: 1px solid #f5c6cb;
	}
	
	.answers-section h2 {
		margin-bottom: 2rem;
		color: #333;
		font-size: 1.8rem;
	}
	
	.empty-state {
		text-align: center;
		padding: 3rem;
		background-color: #f8f9fa;
		border-radius: 8px;
		color: #6c757d;
	}
	
	.answers-grid {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
	
	.answer-card {
		background: white;
		border-radius: 8px;
		padding: 1.5rem;
		box-shadow: 0 2px 8px rgba(0,0,0,0.05);
		border: 1px solid #e9ecef;
		transition: all 0.3s ease;
		display: flex;
		gap: 1rem;
		align-items: flex-start;
	}

	.answer-number {
		background-color: #007bff;
		color: white;
		width: 30px;
		height: 30px;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: bold;
		font-size: 0.9rem;
		flex-shrink: 0;
	}
	
	.answer-text {
		font-size: 1.1rem;
		line-height: 1.5;
		color: #333;
		word-wrap: break-word;
	}
</style>
