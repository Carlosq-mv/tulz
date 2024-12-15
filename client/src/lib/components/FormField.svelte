<script>
  let { type, labelname, placeholder, id, value = $bindable(), children } = $props();
  let showPassword = $state(false);
</script>

<div class="form-control mt-8">
  <label for={id} class="label">
    <span class="label-text">{labelname}</span>
  </label>
  <label class="input input-bordered flex items-center gap-2">
    {#if children}
      {@render children()}
    {/if}
    <input
      class="grow"
      bind:value
      type={type === 'password' && showPassword ? 'text' : type}
      {placeholder}
    />

    <button type="button" onclick={() => (showPassword = !showPassword)}>
      {#if showPassword && type === 'password'}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-eye-off h-6 w-6 opacity-70"
          ><path
            d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"
          /><path d="M14.084 14.158a3 3 0 0 1-4.242-4.242" /><path
            d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"
          /><path d="m2 2 20 20" /></svg
        >
      {:else if !showPassword && type === 'password'}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-eye h-6 w-6 opacity-70"
          ><path
            d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"
          /><circle cx="12" cy="12" r="3" /></svg
        >
      {/if}
    </button>
  </label>
</div>
