<script>
  let { children } = $props();
</script>

<div class="drawer lg:drawer-open">
  <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content flex flex-col p-8 overflow-auto h-screen pb-20">
    <!-- Page content here -->
    {#if children}
      {@render children()}
    {/if}
    <label for="my-drawer-2" class="btn btn-primary drawer-button lg:hidden"> Open drawer </label>
  </div>
  <div class="drawer-side">
    <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label>
    <ul class="menu bg-base-200 text-base-content flex h-screen w-64 flex-col p-4">
      <div class="divider mb-8">
        <div class="flex items-center justify-center">
          <p class="text-md font-black"># channels</p>
        </div>
      </div>
      <!-- Sidebar content here -->
      <li>
        <a href="/contacts" class="text-lg">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="lucide lucide-contact h-5 w-5"
            ><path d="M16 2v2" /><path d="M7 22v-2a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v2" /><path
              d="M8 2v2"
            /><circle cx="12" cy="11" r="3" /><rect
              x="3"
              y="4"
              width="18"
              height="18"
              rx="2"
            /></svg
          >
          Contacts
        </a>
        <a href="/search" class="text-lg">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="lucide lucide-user-search h-5 w-5"
            ><circle cx="10" cy="7" r="4" /><path d="M10.3 15H7a4 4 0 0 0-4 4v2" /><circle
              cx="17"
              cy="17"
              r="3"
            /><path d="m21 21-1.9-1.9" /></svg
          >
          Search
        </a>
      </li>
      <div class="flex-grow"></div>

      <!-- Theme switcher -->
      <div class="divider"></div>
      <div class="mb-24 flex items-center justify-center">
        <label class="flex cursor-pointer gap-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <circle cx="12" cy="12" r="5" />
            <path
              d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"
            />
          </svg>
          <input type="checkbox" value="garden" class="toggle theme-controller scale-75" />
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        </label>
      </div>
    </ul>
  </div>
</div>
