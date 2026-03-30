<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import { PUBLIC_API_URL } from '$env/static/public';
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { toast } from 'svelte-sonner';
	import type { Question } from '../models';

	let { data } = $props();
	let questions: Question[] = $derived(data.questions);

	let text = $state('');
	let submitting = $state(false);

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		submitting = true;
		try {
			const response = await fetch(`${PUBLIC_API_URL}/questions/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ text })
			});
			if (response.ok) {
				text = '';
				toast.success('Question added!');
				await invalidateAll();
			} else {
				const body = await response.json();
				const detail = body?.detail;
				const message = Array.isArray(detail)
					? (detail[0]?.msg ?? 'Validation error.')
					: typeof detail === 'string'
						? detail
						: 'Failed to submit question.';
				toast.error(message);
			}
		} catch {
			toast.error('Error submitting question.');
		} finally {
			submitting = false;
		}
	}
</script>

<div class="space-y-8">
	<!-- Form -->
	<Card>
		<CardHeader>
			<CardTitle>Ask a Question</CardTitle>
		</CardHeader>
		<CardContent>
			<form onsubmit={handleSubmit} class="flex gap-3">
				<input
					id="question"
					type="text"
					bind:value={text}
					placeholder="What would you like to ask?"
					required
					class="flex-1 px-4 py-2 rounded-md border border-input bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
				/>
				<Button type="submit" disabled={submitting}>
					{submitting ? 'Adding…' : 'Add'}
				</Button>
			</form>
		</CardContent>
	</Card>

	<!-- List -->
	<div>
		<h2 class="text-lg font-semibold text-foreground mb-4">All Questions</h2>
		{#if questions.length === 0}
			<Card>
				<CardContent class="text-center py-12 text-muted-foreground">
					No questions yet. Add the first one above.
				</CardContent>
			</Card>
		{:else}
			<ul class="space-y-3">
				{#each questions as question, i}
					<li
						class="animate-in fade-in-0 slide-in-from-bottom-2 duration-200"
						style="animation-delay: {i * 40}ms"
					>
						<Card class="transition-shadow duration-200 hover:shadow-sm">
							<CardContent class="flex items-center justify-between gap-4 py-4">
								<a
									href="/answers/{question.id}"
									class="text-primary underline-offset-4 hover:underline transition-colors"
								>
									{question.text}
								</a>
								<Button href="/answers/{question.id}" variant="outline" size="sm" class="shrink-0">
									View Answers →
								</Button>
							</CardContent>
						</Card>
					</li>
				{/each}
			</ul>
		{/if}
	</div>
</div>
