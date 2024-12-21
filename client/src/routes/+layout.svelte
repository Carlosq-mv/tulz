<script>
  import '../app.css';
  import { onMount, setContext } from 'svelte';
  import { getCurrentAuthUser, refreshToken } from '$lib/api/auth';
  import { goto } from '$app/navigation';
  import { writable } from 'svelte/store';

  let { children } = $props();

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
        await refreshToken();
        // call once again the end point to get current user
        res = await getCurrentAuthUser();
        data = await res.json();
      }

      // set the response data in a store
      userStore.set(data);
      return data;
    } catch (error) {
      userStore.set(null);
      return null;
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

{@render children()}
