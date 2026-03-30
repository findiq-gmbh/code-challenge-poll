<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import { page } from '$app/state';
	import { PUBLIC_API_URL } from '$env/static/public';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { toast } from 'svelte-sonner';
	import type { Answer, Question } from '../../models';

	let { data } = $props();
	let question: Question | null = $derived(data.question);
	let answers: Answer[] = $derived(data.answers);

	let text = $state('');
	let submitting = $state(false);

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		submitting = true;
		try {
			const response = await fetch(`${PUBLIC_API_URL}/questions/${page.params.id}/answers`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ text })
			});
			if (response.ok) {
				text = '';
				toast.success('Answer submitted!');
				await invalidateAll();
			} else {
				const body = await response.json();
				const detail = body?.detail;
				const message = Array.isArray(detail)
					? (detail[0]?.msg ?? 'Validation error.')
					: typeof detail === 'string'
						? detail
						: 'Failed to submit answer.';
				toast.error(message);
			}
		} catch {
			toast.error('Error submitting answer.');
		} finally {
			submitting = false;
		}
	}
</script>

<div class="space-y-8">
	<!-- Question heading -->
	{#if question}
		<div>
			<Button href="/questions" variant="ghost" size="sm" class="-ml-2 mb-1">
				← All Questions
			</Button>
			<h1 class="mt-1 text-2xl font-bold text-foreground">{question.text}</h1>
		</div>
	{:else}
		<p class="text-destructive">Question not found.</p>
	{/if}

	<!-- Answer form -->
	<Card>
		<CardHeader>
			<CardTitle class="text-base">Submit an Answer</CardTitle>
		</CardHeader>
		<CardContent>
			<form onsubmit={handleSubmit} class="flex gap-3">
				<input
					id="answer"
					type="text"
					bind:value={text}
					placeholder="Your answer…"
					required
					class="flex-1 px-4 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
				/>
				<Button type="submit" disabled={submitting}>
					{submitting ? 'Submitting…' : 'Submit'}
				</Button>
			</form>
		</CardContent>
	</Card>

	<!-- Answers list -->
	<div>
		<h2 class="text-base font-semibold text-foreground mb-4">
			{answers.length}
			{answers.length === 1 ? 'Answer' : 'Answers'}
		</h2>
		{#if answers.length === 0}
			<Card>
				<CardContent class="text-center py-10 text-muted-foreground">
					No answers yet. Be the first!
				</CardContent>
			</Card>
		{:else}
			<ul class="space-y-2">
				{#each answers as answer, i (answer.id)}
					<li
						class="animate-in fade-in-0 slide-in-from-bottom-2 duration-200"
						style="animation-delay: {i * 40}ms"
					>
						<Card class="transition-shadow duration-200 hover:shadow-sm">
							<CardContent class="py-3 text-foreground">
								{answer.text}
							</CardContent>
						</Card>
					</li>
				{/each}
			</ul>
		{/if}
	</div>
</div>
