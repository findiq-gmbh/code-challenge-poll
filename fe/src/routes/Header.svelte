<script lang="ts">
import { page } from "$app/state";
import { mode, toggleMode } from "mode-watcher";
import { Moon, Sun } from "lucide-svelte";

const links = [
  { href: "/questions", label: "Questions" },
  { href: "/visits", label: "Visits" },
];
</script>

<header class="bg-background border-b border-border shadow-sm" style="view-transition-name: site-header">
	<div class="max-w-3xl mx-auto px-4 h-14 flex items-center justify-between">
		<a href="/" class="text-lg font-bold text-foreground tracking-tight hover:text-primary transition-colors">
			Polling
		</a>
		<div class="flex items-center gap-1">
			<nav class="flex items-center gap-1">
				{#each links as link (link.label)}
					<a
						href={link.href}
						class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors
							{page.url.pathname.startsWith(link.href)
								? 'bg-primary/10 text-primary'
								: 'text-muted-foreground hover:text-foreground hover:bg-muted'}"
					>
						{link.label}
					</a>
				{/each}
			</nav>
			<button
				onclick={toggleMode}
				aria-label="Toggle theme"
				class="ml-2 p-1.5 rounded-md text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
			>
				{#if mode.current === "dark"}
					<Sun size={16} />
				{:else}
					<Moon size={16} />
				{/if}
			</button>
		</div>
	</div>
</header>
