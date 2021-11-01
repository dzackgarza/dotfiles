<apply template="base">
  <bind tag="body-main">
    <div class="flex h-screen bg-gray-200">
      <div class="container m-auto max-w-screen-sm rounded-lg">
        <div class="flex-1 w-full overflow-x-auto">
          <main class="px-4 py-4 border-2 border-pink-300 hover:border-pink-500 rounded bg-white">
            <h1 class="flex items-end justify-center p-3 text-5xl font-extrabold text-black rounded">
              <a class="z-40 tracking-tighter ">
                <ema:note:title />
              </a>
            </h1>
            <aside class="flex items-end justify-center italic mb-4 text-gray-500 text-sm">
            </aside>
            <apply template="components/note-body" />
          </main>
      </div>
      </div>
    </div>
  </bind>
</apply>
