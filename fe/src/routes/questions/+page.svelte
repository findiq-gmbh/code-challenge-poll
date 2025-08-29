<script lang="ts">
	import { onMount } from 'svelte';
	
	const API_BASE_URL = 'http://localhost:8000';

	let questions: Question[] = [];
	let loading = true;
	let error = '';
	let text = '';
	let message = '';

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		message = '';
		
		const trimmedText = text.trim();
		if (!trimmedText) {
			message = 'Question text cannot be empty';
			return;
		}

		try {
			const response = await fetch(`${API_BASE_URL}/questions/`, {
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
				const errorData = await response.json();
            	message = `Failed to submit question: ${errorData.detail}`;

			}
		} catch (error) {
			message = 'Error submitting question. Please check your connection.';
		}
	}

	async function fetchQuestions() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${API_BASE_URL}/questions/`);
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

<div>
	<h1>Poll Questions</h1>
	
	<div class="form-section">
		<h2>Ask a Question</h2>
		<form on:submit|preventDefault={handleSubmit} class="question-form">
			<label for="question">Question:</label>
			<div class="input-group">
				<input 
					id="question" 
					type="text" 
					bind:value={text} 
					required
					minlength="1"
					placeholder="Write your question"
					class="question-input"
				/>
				<button type="submit" class="submit-btn">
					Ask Question
				</button>
			</div>
		</form>
		{#if message}
			<div class="message" class:success={message.includes('successfully')} class:error={!message.includes('successfully')}>
				{message}
			</div>
		{/if}
	</div>

	<div class="questions-section">
		{#if loading}
			<div class="loading-state">
				<div class="spinner"></div>
				<p>Loading questions...</p>
			</div>
		{:else if error}
			<div class="error-state">
				{error}
			</div>
		{:else}
			<h2>All Questions ({questions.length})</h2>
			{#if questions.length === 0}
				<div class="empty-state">
					<p>No questions yet!</p>
				</div>
			{:else}
				<div class="questions-grid">
					{#each questions as question}
						<div class="question-card">
							<div class="question-text">{question.text}</div>
							<a href="/questions/{question.id}/answers" class="answers-link">
								View Answers
							</a>
						</div>
					{/each}
				</div>
			{/if}
		{/if}
	</div>
</div>


<style>
	h1 {
		text-align: center;
		margin-bottom: 2rem;
		color: #333;
		font-size: 2.5rem;
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
	
	.question-form {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
	
	.input-group {
		display: flex;
		gap: 1rem;
		align-items: center;
	}
	
	.question-input {
		flex: 1;
		padding: 1rem;
		border: 2px solid #e9ecef;
		border-radius: 8px;
		font-size: 1rem;
		transition: border-color 0.3s ease;
	}
	
	.question-input:focus {
		outline: none;
		border-color: #007bff;
		box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
	}
	
	.question-input:disabled {
		background-color: #f8f9fa;
		color: #6c757d;
	}
	
	.submit-btn {
		padding: 1rem 2rem;
		background-color: #007bff;
		color: white;
		border: none;
		border-radius: 8px;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.3s ease;
		white-space: nowrap;
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
	
	.questions-section h2 {
		margin-bottom: 2rem;
		color: #333;
		font-size: 1.8rem;
	}
	
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
	
	.empty-state {
		text-align: center;
		padding: 3rem;
		background-color: #f8f9fa;
		border-radius: 8px;
		color: #6c757d;
	}
	
	.questions-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 1.5rem;
	}
	
	.question-card {
		background: white;
		border-radius: 12px;
		padding: 1.5rem;
		box-shadow: 0 2px 12px rgba(0,0,0,0.05);
		border: 1px solid #e9ecef;
		transition: all 0.3s ease;
	}
	
	.question-text {
		font-size: 1.1rem;
		line-height: 1.5;
		color: #333;
		margin-bottom: 1rem;
		min-height: 3em;
	}
	
	.answers-link {
		display: inline-flex;
		align-items: center;
		padding: 0.75rem 1.5rem;
		background-color: #007bff;
		color: white;
		text-decoration: none;
		border-radius: 25px;
		font-weight: 500;
		transition: all 0.3s ease;
		font-size: 0.9rem;
	}
</style>
