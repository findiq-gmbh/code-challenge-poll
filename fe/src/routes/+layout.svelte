<script lang="ts">
import { afterNavigate, beforeNavigate, onNavigate } from "$app/navigation";

import { ModeWatcher } from "mode-watcher";
import Header from "./Header.svelte";
import { Toaster } from "$lib/components/ui/sonner";
import "../app.css";

let { children } = $props();
let loading = $state(false);

beforeNavigate(() => {
  loading = true;
});
afterNavigate(() => {
  loading = false;
});

onNavigate((navigation) => {
  if (!document.startViewTransition) return;
  // Hide the loading bar before startViewTransition captures its screenshot
  loading = false;
  return new Promise((resolve) => {
    document.startViewTransition(async () => {
      resolve();
      await navigation.complete;
    });
  });
});
</script>

<ModeWatcher />
<div class="min-h-screen flex flex-col bg-background text-foreground">
	{#if loading}
		<div class="fixed top-0 left-0 right-0 h-0.5 bg-primary animate-pulse z-50"></div>
	{/if}
	<Header />
	<main class="flex-1 w-full max-w-3xl mx-auto px-4 py-8">
		{@render children()}
	</main>
	<Toaster richColors />
</div>
