<script>
  import { getContext } from 'svelte';
  import { goto } from '$app/navigation';
  import Navbar from '$lib/components/Navbar.svelte';
  import Sidebar from '$lib/components/Sidebar.svelte';
  const userStore = getContext('auth');

  // Subscribe to the store so that it updates reactively
  let user = $state();
  userStore.subscribe((value) => {
    user = value; // Update the `user` variable wheneearer the store changes
  });
  let users = $state([]);
</script>

<div>
  <p>This is the home page</p>
  {#if user}
    <p>Welcome, {user.username}</p>
  {:else}
    <p>No use data</p>
  {/if}
</div>
