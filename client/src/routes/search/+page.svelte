<script>
  import { search } from '$lib/api/user';
  import { addContact } from '$lib/api/contact';
  import Alert from '$lib/components/Alert.svelte';
  import { AlertType } from '$lib/constants/enums';

  let contact = $state();
  let searchResult = $state('');
  let errorMessage = $state('');
  let successMessage = $state('');
  let addContactErrorMessage = $state('');

  function clearMessages() {
    errorMessage = '';
    successMessage = '';
    addContactErrorMessage = '';
  }
  async function handleSearch(event) {
    event.preventDefault();
    try {
      const res = await search(contact);
      clearMessages();
      searchResult = res;
      console.log(res);
    } catch (error) {
      searchResult = '';
      errorMessage = error;
      console.error(error);
    }
  }

  async function handleAddContact(data) {
    const payload = {
      current_user_id: 9999,
      friend_id: data.id
    };
    try {
      const res = await addContact(payload);
      addContactErrorMessage = '';
      successMessage = `Succesfully requested to add ${data.username} as contact.`;
      console.log(res);
    } catch (error) {
      successMessage = '';
      addContactErrorMessage = error;
      console.log(error);
    }
  }
</script>

<div>
  <div class="mb-6 text-center">
    <h1 class="text-3xl font-semibold">Find Your Contacts</h1>
    <p class="m-8 text-lg">
      Search for a user by their username to add them to your contact list. Connect and stay in
      touch!
    </p>

    <div class="flex items-center justify-center">
      <figure class="h-64 w-64">
        <img src="/connections.png" alt="conntection" class="h-full w-full object-cover" />
      </figure>
    </div>
  </div>

  <div>
    <form onsubmit={handleSearch}>
      <label class="input input-bordered flex items-center gap-2">
        <input type="text" class="grow" placeholder="Search" bind:value={contact} />
        <button type="submit" aria-label="search-btn">
          <img src="icons/search.svg" alt="search icon" class="text-white" />
        </button>
      </label>
    </form>

    {#if searchResult}
      <div class="card m-8 rounded-lg border border-gray-200 shadow-xl">
        <div class="card-body p-6">
          <h2 class="card-title mb-2 text-2xl font-bold">Search Results:</h2>
          <p class="mb-1 text-lg">
            <span class="text-lg font-semibold">Name:</span>
            {searchResult.name}
          </p>
          <p class="mb-3 text-lg">
            <span class="text-lg font-semibold">Username:</span>
            {searchResult.username}
          </p>
          <div class="card-actions flex items-center justify-center">
            <button
              class="btn btn-primary"
              onclick={() => {
                handleAddContact(searchResult);
              }}
            >
              <img src="icons/add-contact.svg" alt="add contact icon" />
              Request Contact
            </button>
            {#if successMessage}
              <Alert type={AlertType.SUCCESS} message={successMessage} />
            {:else if addContactErrorMessage}
              <Alert type={AlertType.ERROR} message={addContactErrorMessage} />
            {/if}
          </div>
        </div>
      </div>
    {:else if errorMessage}
      <Alert type={AlertType.ERROR} message={errorMessage} />
    {/if}
  </div>
</div>
