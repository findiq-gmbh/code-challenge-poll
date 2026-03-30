<script lang="ts">
	import { Badge } from '$lib/components/ui/badge';
	import { Card, CardContent } from '$lib/components/ui/card';
	import type { QuestionWithVisits } from './+page';

	let { data } = $props();
	let questions: QuestionWithVisits[] = $derived(data.questions);
</script>

<div class="space-y-6">
	<h1 class="text-2xl font-bold text-foreground">Question Visits</h1>

	{#if questions.length === 0}
		<Card>
			<CardContent class="text-center py-12 text-muted-foreground">
				No visits recorded yet.
			</CardContent>
		</Card>
	{:else}
		<ul class="space-y-3">
			{#each questions as q, i}
				<li class="animate-in fade-in-0 slide-in-from-bottom-2 duration-200" style="animation-delay: {i * 40}ms">
					<Card class="transition-shadow duration-200 hover:shadow-sm">
						<CardContent class="flex items-center justify-between gap-4 py-4">
							<a href="/answers/{q.id}" class="text-primary underline-offset-4 hover:underline transition-colors">
								{q.text}
							</a>
							<Badge variant="secondary" class="shrink-0">
								{q.visit_count} {q.visit_count === 1 ? 'visit' : 'visits'}
							</Badge>
						</CardContent>
					</Card>
				</li>
			{/each}
		</ul>
	{/if}
</div>
