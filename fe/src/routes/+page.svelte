<script>
	import Container from '$lib/components/Container.svelte';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<Container alignCenter>
	<h1>Welcome 👋</h1>
	<p>Find and ask questions from the community!</p>
	<a href="/questions" class="button">Go to Questions</a>
</Container>

<style>
	.button {
		display: inline-block;
		margin-top: 1rem;
		padding: 0.5rem 1rem;
		background: #0070f3;
		color: white;
		text-decoration: none;
		border-radius: 4px;
	}
	.button:hover {
		background: #005ac1;
	}
</style>
