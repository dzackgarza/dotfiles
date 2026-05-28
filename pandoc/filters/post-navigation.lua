-- =============================================================================
-- POST RECOMMENDATION SYSTEM & PAGE NAVIGATION
-- =============================================================================
--
-- This filter implements the quality "You May Also Enjoy" post-recommendation system.
--
-- RECOMMENDATION ALGORITHM:
-- 1. Identify the current post and build a lowercase, case-insensitive set of its tags.
-- 2. Scan all other blog posts and calculate a "tag overlap score" (number of matching tags).
-- 3. Filter out the current post, sorting all other posts by:
--    a. Tag overlap score (highest score first)
--    b. Post publication date (newest first, if scores are equal)
-- 4. Select the top 4 posts as recommendations.
-- 5. FALLBACK MECHANISM: If tag overlap yields fewer than 4 posts (or if the current post
--    has no tags), fill the remaining slots with the overall newest blog posts (excluding
--    the current post and already selected recommendations). This guarantees exactly 4
--    cards are always rendered.
-- =============================================================================

local data_dir = os.getenv("PANDOC_SITE_DATA_DIR")

local function fail(message)
  error("[post-navigation.lua] " .. message)
end

local function read_file(file_path)
  local handle = io.open(file_path, "r")
  if not handle then
    fail("unable to read " .. file_path)
  end
  local contents = handle:read("*a")
  handle:close()
  return contents
end

local function decode_json(file_path)
  return pandoc.json.decode(read_file(file_path))
end

local function escape_html(str)
  if not str then return "" end
  str = tostring(str)
  str = str:gsub("&", "&amp;")
  str = str:gsub('"', "&quot;")
  str = str:gsub("<", "&lt;")
  str = str:gsub(">", "&gt;")
  return str
end

local function make_link(href, label, direction)
  local text = direction == "prev" and "Previous" or "Next"
  return '<a href="' .. escape_html(href) .. '" class="pagination--pager" title="' .. escape_html(label) .. '">'
    .. text .. '</a>'
end

local function make_related_card(post, blog_base, base_url)
  local img_src = post.image or "/assets/images/bigo.png"
  if img_src:sub(1,1) == "/" and img_src:sub(2,2) ~= "/" then
    img_src = base_url .. img_src
  end
  local img_html = '<div class="archive__item-teaser"><img src="' .. escape_html(img_src) .. '" alt=""></div>'
  local read_html = ""
  if post.readMinutes then
    read_html = '<span class="page__meta-readtime"><i class="far fa-clock" aria-hidden="true"></i> ' .. tostring(post.readMinutes) .. ' minute read</span>'
  end
  local excerpt_html = ""
  if post.excerpt then
    excerpt_html = '<p class="archive__item-excerpt">' .. escape_html(post.excerpt) .. '</p>'
  end
  return [[
<div class="grid__item">
  <article class="archive__item">]] .. img_html .. [[
    <h2 class="archive__item-title no_toc"><a href="]] .. blog_base .. "/" .. post.slug .. '">' .. escape_html(post.title) .. [[</a></h2>
    <p class="page__meta">]] .. read_html .. [[</p>
    ]] .. excerpt_html .. [[
  </article>
</div>]]
end

function Pandoc(doc)
  if not data_dir then
    return nil
  end

  local slug_meta = doc.meta["pg_slug"]
  if not slug_meta then
    return nil  -- not a blog post
  end
  local slug = pandoc.utils.stringify(slug_meta)

  local posts
  local ok, result = pcall(decode_json, data_dir .. "/posts.json")
  if not ok then
    return nil
  end
  posts = result

  -- Find current post index (posts are sorted newest-first)
  local current_idx
  for i, post in ipairs(posts) do
    if post.slug == slug then
      current_idx = i
      break
    end
  end
  if not current_idx then
    return nil
  end

  local base_url = os.getenv("BASE_URL") or ""
  local blog_base = base_url .. "/blog"
  local html_parts = {}

  -- Previous / next by date
  if current_idx > 1 then
    local prev = posts[current_idx - 1]
    table.insert(html_parts, make_link(blog_base .. "/" .. prev.slug, prev.title, "prev"))
  end
  if current_idx < #posts then
    local next_post = posts[current_idx + 1]
    table.insert(html_parts, make_link(blog_base .. "/" .. next_post.slug, next_post.title, "next"))
  end

  -- Related by tag overlap (Case-Insensitive matching)
  local current = posts[current_idx]
  local tag_set = {}
  if current.tags then
    for _, t in ipairs(current.tags) do
      tag_set[t:lower()] = true
    end
  end
  local related = {}
  local seen = {}
  for idx, post in ipairs(posts) do
    if idx ~= current_idx then
      local score = 0
      if post.tags then
        for _, t in ipairs(post.tags) do
          if tag_set[t:lower()] then
            score = score + 1
          end
        end
      end
      if score > 0 then
        table.insert(related, { post = post, score = score })
      end
    end
  end

  -- Sort related posts by overlap score (highest first), then by date (newest first)
  table.sort(related, function(a, b)
    if a.score ~= b.score then return a.score > b.score end
    return a.post.date > b.post.date
  end)

  local final_related = {}
  -- 1. Add posts with tag overlap
  for _, r in ipairs(related) do
    if #final_related < 4 then
      table.insert(final_related, r.post)
      seen[r.post.slug] = true
    end
  end

  -- 2. Fallback to newest posts to fill up to 4 recommendations
  if #final_related < 4 then
    for _, post in ipairs(posts) do
      if post.slug ~= current.slug and not seen[post.slug] then
        if #final_related < 4 then
          table.insert(final_related, post)
          seen[post.slug] = true
        end
      end
    end
  end

  local related_html = {}
  for _, r_post in ipairs(final_related) do
    table.insert(related_html, make_related_card(r_post, blog_base, base_url))
  end

  local all_html = {}

  if #html_parts > 0 then
    table.insert(all_html, '<nav class="post-nav" aria-label="Post navigation">'
      .. table.concat(html_parts, "\n") .. '</nav>')
  end

  if #related_html > 0 then
    table.insert(all_html, [[
<div class="page__related">
  <h4 class="page__related-title">You May Also Enjoy</h4>
  <div class="grid__wrapper">]] .. table.concat(related_html, "\n") .. [[</div>
</div>]])
  end

  if #all_html == 0 then
    return nil
  end

  local wrapper = pandoc.Div(
    { pandoc.RawBlock("html", table.concat(all_html, "\n")) },
    pandoc.Attr("", { "post-nav-wrapper" })
  )

  local blocks = doc.blocks
  table.insert(blocks, wrapper)
  return pandoc.Pandoc(blocks, doc.meta)
end
