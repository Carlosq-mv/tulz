<script>
  let { message } = $props();
</script>

<div class="group relative flex items-center justify-center p-4 text-center">
  <button class="btn btn-circle btn-ghost mr-4">
    <img src="icons/sad-face.svg" alt="sad-face" />
  </button>
  <span
    class="absolute left-1/2 top-14 -translate-x-1/2 transform rounded-xl bg-gray-500 px-2 py-1 text-sm text-white opacity-0 transition-opacity duration-300 group-hover:opacity-100"
  >
    Dont't be sad my friend!
  </span>
  {message}
</div>
