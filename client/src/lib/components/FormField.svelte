<script>
	let { type, labelname, placeholder, id, value = $bindable(), children } = $props();
</script>

<div class="form-control mt-8">
	<label for={id} class="label">
		<span class="label-text">{labelname}</span>
	</label>
	<label class="input input-bordered flex items-center gap-2">
		{#if children}
			{@render children()}
		{/if}
		<input class="grow" bind:value={value} {type} {placeholder} />
	</label>
</div>