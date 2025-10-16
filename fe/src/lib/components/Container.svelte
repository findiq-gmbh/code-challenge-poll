<script lang="ts">
	export let alignCenter = false;

	const classes = `container${alignCenter ? ' center' : ''}`;
</script>

<div class={classes}>
	<slot />
</div>

<style>
	.container {
		width: 780px;
		max-width: 90%;
		margin: 3rem auto;
		background: white;
		padding: 2rem;
		border-radius: 12px;
		box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
	}
	.center {
		text-align: center;
	}
</style>
