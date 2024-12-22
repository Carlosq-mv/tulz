<script>
  import '../app.css';
  import { onMount, setContext } from 'svelte';
  import { getCurrentAuthUser, refreshToken } from '$lib/api/auth';
  import { goto } from '$app/navigation';
  import { writable } from 'svelte/store';
  import { page } from '$app/stores';

  import { logout } from '$lib/api/auth';
  import Navbar from '$lib/components/Navbar.svelte';
  import Sidebar from '$lib/components/Sidebar.svelte';
  import { redirect } from '@sveltejs/kit';

  let { children } = $props();
  let excludedRoutes = ['/login', '/signup'];

  // reactive variable 'user' that initialized will be used to hold the authenticated user data.
  let user = $state(null);

  // a writable store allows us to update the value of 'userStore' and listen to its changes.
  // this store can be used globally to track and update the current user data across components.
  const userStore = writable(null);

  async function handleAuthContext() {
    try {
      // call end point to get current user
      let res = await getCurrentAuthUser();
      // transform the data to json format
      let data = await res.json();

      // check if Unauthorized status
      if (res.status === 401) {
        // call end point to refresh jwt token
        const refRes = await refreshToken();
        // if Unauthorized status for refreshToken, it means user doesn't have a refreshToken
        // so no need to continue
        if (refRes.status === 401) {
          return;
        }
        // call once again the end point to get current user
        res = await getCurrentAuthUser();
        data = await res.json();
      }

      // set the response data in a store
      userStore.set(data);
      // console.log(data)
      return data;
    } catch (error) {
      userStore.set(null);
      return null;
    }
  }

  async function handleLogout() {
    console.log('logout clicked');
    try {
      const res = await logout();
      console.log(res);
      user = null;
      goto('/login');
    } catch (error) {
      console.log(error);
    }
  }

  $effect(async () => {
    user = await handleAuthContext();
    // if (!user) {
    //   goto('/login'); // Redirect to the login page
    // }
    // console.log($state.snapshot(user));
  });

  // set the 'userStore' writable store as context with the key 'auth'.
  // this makes 'userStore' accessible to all descendant components in the component tree that use 'getContext' with the same key ('auth').
  // now able to share the current user data (stored in 'userStore') across multiple components without prop-drilling.
  setContext('auth', userStore);
</script>

{#if !excludedRoutes.includes($page.url.pathname)}
  <div class="flex h-screen flex-col">
    <!-- Navbar -->
    <Navbar
      logout={handleLogout}
      class="flex h-16 items-center justify-between bg-blue-500 px-4 shadow-md"
    />

    <div class="flex flex-grow overflow-hidden">
      <!-- Sidebar -->
      <Sidebar class="w-64 flex-shrink-0 overflow-y-auto bg-gray-200 p-4">
        {@render children()}
      </Sidebar>
    </div>
  </div>
{:else}
  {@render children()}
{/if}
