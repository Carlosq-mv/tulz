<script>
  import { goto } from '$app/navigation';
  import FormField from '$lib/components/FormField.svelte';
  import Alert from '$lib/components/Alert.svelte';
  import { login } from '$lib/api/auth';

  let form = $state({
    username: '',
    email: '',
    password: ''
  });
  let loading = $state(false);
  let errorMessage = $state('');

  async function handleLogin(event) {
    loading = true;
    event.preventDefault();

    try {
      const res = await login(form);
      console.log(res);
      form.username = '';
      form.email = '';
      form.password = '';
      errorMessage = '';
      goto('/home')
    } catch (error) {
      console.log(error);
      errorMessage = error;
    } finally {
      loading = false;
    }
  }
</script>

<div class="bg-base-200 flex min-h-screen items-center justify-center">
  <div class="card bg-base-100 lg:card-side min-h-[75vh] w-full max-w-7xl shadow-xl">
    <figure class="lg:w-3/5">
      <img src="/wood.jpg" alt="wood" class="h-full w-full object-cover" />
    </figure>
    <div class="card-body lg:w-1/2">
      <h2 class="prose card-title text-accent mb-6 text-4xl font-bold">Login to Tulz</h2>
      {#if errorMessage}
        <Alert {errorMessage} />
      {/if}
      <form onsubmit={handleLogin} method="POST">
        <FormField
          type="text"
          labelname="Username"
          placeholder="Enter Username"
          id="username"
          bind:value={form.username}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="lucide lucide-user h-4 w-4 opacity-70"
          >
            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        </FormField>

        <FormField
          type="email"
          labelname="Email"
          placeholder="example@example.com"
          id="email"
          bind:value={form.email}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 16 16"
            fill="currentColor"
            class="h-4 w-4 opacity-70"
          >
            <path
              d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z"
            />
            <path
              d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z"
            />
          </svg>
        </FormField>

        <FormField
          type="password"
          labelname="Password"
          placeholder="Enter password"
          id="password"
          bind:value={form.password}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 16 16"
            fill="currentColor"
            class="h-4 w-4 opacity-70"
          >
            <path
              fill-rule="evenodd"
              d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z"
              clip-rule="evenodd"
            />
          </svg>
        </FormField>

        <div class="form-control mt-10">
          <button type="submit" class="btn btn-primary">
            {#if loading}
              <span class="loading loading-spinner loading-md"></span>
            {:else}
              Login
            {/if}
          </button>
        </div>
      </form>
      <div class="divider pt-8">OR</div>
      <div class="prose text-center">
        <p>Don't have an account?</p>
        <a href="/signup" class="link link-primary">Sign up now</a>
      </div>
    </div>
  </div>
</div>
