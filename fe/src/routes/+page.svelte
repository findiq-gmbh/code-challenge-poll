<svelte:head>
	<title>Ask Questions, Get Answers</title>
	<meta name="description" content="" />
</svelte:head>

<div class="home-container">
	<section class="hero">
		<h1>Polling Application</h1>
		<p class="hero-subtitle">
			Application that allows the creation and answering of questions
		</p>
		
		<div class="action-buttons">
			<a href="/questions" class="primary-btn">Ask a Question</a>
			<a href="/questions/statistics" class="secondary-btn">View Statistics</a>
		</div>
	</section>
</div>

<style>
	.home-container {
		max-width: 1000px;
		margin: 0 auto;
		padding: 2rem 1rem;
	}
	
	.hero {
		text-align: center;
		padding: 4rem 2rem;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		border-radius: 20px;
		margin-bottom: 4rem;
		box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
	}
	
	.hero h1 {
		font-size: 3rem;
		margin-bottom: 1rem;
		font-weight: 700;
	}
	
	.hero-subtitle {
		font-size: 1.3rem;
		margin-bottom: 2rem;
		opacity: 0.9;
		line-height: 1.5;
		max-width: 600px;
		margin-left: auto;
		margin-right: auto;
	}
	
	.action-buttons {
		display: flex;
		gap: 1rem;
		justify-content: center;
		flex-wrap: wrap;
	}
	
	.primary-btn {
		display: inline-flex;
		align-items: center;
		padding: 1rem 2rem;
		background-color: white;
		color: #667eea;
		text-decoration: none;
		border-radius: 50px;
		font-weight: 600;
		font-size: 1.1rem;
		transition: all 0.3s ease;
		box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
	}
	
	.primary-btn:hover {
		transform: translateY(-3px);
		box-shadow: 0 8px 25px rgba(255, 255, 255, 0.3);
		background-color: #f8f9ff;
	}
	
	.secondary-btn {
		display: inline-flex;
		align-items: center;
		padding: 1rem 2rem;
		background-color: transparent;
		color: white;
		text-decoration: none;
		border: 2px solid white;
		border-radius: 50px;
		font-weight: 600;
		font-size: 1.1rem;
		transition: all 0.3s ease;
	}
</style>
