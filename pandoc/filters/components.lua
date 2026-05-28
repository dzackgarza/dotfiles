-- Render Pandoc fenced Div component declarations into static document blocks.
-- Data is prepared by scripts/compile.cjs in .generated/pandoc-data as JSON.
-- Components emit DOM placeholders that React mounts into at runtime.

local data_dir = os.getenv("PANDOC_SITE_DATA_DIR")

local function fail(message)
  error("[components.lua] " .. message)
end

local function read_file(file_path)
  local handle = io.open(file_path, "r")
  if not handle then
    fail("unable to read data file: " .. file_path)
  end
  local contents = handle:read("*a")
  handle:close()
  return contents
end

local function decode_json(file_path)
  return pandoc.json.decode(read_file(file_path))
end

local function database_path(source)
  if not data_dir then
    fail("PANDOC_SITE_DATA_DIR is required")
  end
  if not source then
    fail("component requires a source attribute")
  end
  local database_name = source:match("^databases/([%w%._%-]+)%.toml$")
  if not database_name then
    fail("invalid component source: " .. source)
  end
  return data_dir .. "/databases/" .. database_name .. ".json"
end

local function has_value(field, expected)
  if type(field) == "table" then
    for _, value in ipairs(field) do
      if value == expected then
        return true
      end
    end
    return false
  end
  return field == expected
end

local function parse_filter(filter)
  local conditions = {}
  if not filter or filter == "" then
    return conditions
  end
  for condition in filter:gmatch("[^,]+") do
    local key, value = condition:match("^%s*([%w_-]+)%s*=%s*([^%s]+)%s*$")
    if not key or not value then
      fail("invalid component filter: " .. filter)
    end
    table.insert(conditions, { key = key, value = value })
  end
  return conditions
end

local function filter_items(items, filter)
  local conditions = parse_filter(filter)
  if #conditions == 0 then
    return items
  end
  local filtered = {}
  for _, item in ipairs(items) do
    for _, condition in ipairs(conditions) do
      if has_value(item[condition.key], condition.value) then
        table.insert(filtered, item)
        break
      end
    end
  end
  return filtered
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

local function render_collection(el)
  local database = decode_json(database_path(el.attributes.source))
  local items = filter_items(database.items or {}, el.attributes.filter)
  local types = database.types or {}
  local columns = tonumber(el.attributes.columns) or 3
  local rows = tonumber(el.attributes.rows) or 3
  local layout = el.attributes.layout or "grid"
  local filterable = el.attributes.filterable == "true"

  local data = {
    items = items,
    types = types,
    columns = columns,
    rows = rows,
    layout = layout,
    filterable = filterable,
  }

  local json = pandoc.json.encode(data)

  return pandoc.Div(
    { pandoc.RawBlock("html", "<!-- collection placeholder -->") },
    pandoc.Attr("", {}, {
      ["data-component"] = "AcademicCollection",
      ["data-json"] = json,
    })
  )
end

local function render_link_group(el)
  local group_id = el.attributes["group-id"]
  if not group_id then
    fail("link-group component requires group-id")
  end
  local database = decode_json(database_path(el.attributes.source))
  for _, group in ipairs(database.groups or {}) do
    if group.id == group_id then
      local blocks = { pandoc.Header(3, group.title or "") }
      if group.description and group.description ~= "" then
        table.insert(blocks, pandoc.Para({ pandoc.Str(group.description) }))
      end
      if group.links and #group.links > 0 then
        local items = {}
        for _, link in ipairs(group.links) do
          local href = tostring(link.href or "")
          local base_url = os.getenv("BASE_URL") or ""
          if href:sub(1,1) == "/" and href:sub(2,2) ~= "/" then
            href = base_url .. href
          end
          table.insert(
            items,
            { pandoc.Plain({ pandoc.Link(tostring(link.label or ""), href) }) }
          )
        end
        table.insert(blocks, pandoc.BulletList(items))
      end
      return pandoc.Div(
        blocks,
        pandoc.Attr("", { "content-link-group" }, { ["data-rendered-component"] = "link-group" })
      )
    end
  end
  fail("link group not found: " .. group_id)
end

local function render_gallery(el)
  local gallery_id = el.attributes["gallery-id"]
  if not gallery_id then
    fail("gallery-grid component requires gallery-id")
  end
  local database = decode_json(database_path(el.attributes.source))
  for _, gallery in ipairs(database.items or {}) do
    if gallery.id == gallery_id then
      local figures = {}
      for _, image in ipairs(gallery.images or {}) do
        if image.src then
          table.insert(
            figures,
            pandoc.Para({ pandoc.Image(tostring(image.caption or ""), image.src) })
          )
        elseif image.url then
          table.insert(
            figures,
            pandoc.Para({ pandoc.Link(tostring(image.caption or ""), image.url) })
          )
        else
          fail("gallery item requires src or url")
        end
      end
      local json = pandoc.json.encode({
        images = gallery.images or {},
      })
      return pandoc.Div(
        { pandoc.RawBlock("html", "<!-- gallery placeholder -->") },
        pandoc.Attr("", {}, {
          ["data-component"] = "GalleryGrid",
          ["data-json"] = json,
        })
      )
    end
  end
  fail("gallery not found: " .. gallery_id)
end

local function render_blog_listing()
  if not data_dir then
    fail("PANDOC_SITE_DATA_DIR is required")
  end
  local posts = decode_json(data_dir .. "/posts.json")
  local base_url = os.getenv("BASE_URL") or ""
  local blog_base = base_url .. "/blog"
  local data = { posts = posts, basePath = blog_base }
  local json = pandoc.json.encode(data)
  return pandoc.Div(
    { pandoc.RawBlock("html", "<!-- blog listing placeholder -->") },
    pandoc.Attr("", {}, {
      ["data-component"] = "BlogListing",
      ["data-json"] = json,
    })
  )
end

function Div(el)
  if not el.classes:includes("component") then
    return nil
  end

  local component_type = el.attributes.type
  if not component_type then
    fail(".component div missing type attribute")
  end

  if component_type == "collection" then
    return render_collection(el)
  elseif component_type == "link-group" then
    return render_link_group(el)
  elseif component_type == "gallery-grid" then
    return render_gallery(el)
  elseif component_type == "blog-listing" then
    return render_blog_listing()
  end

  fail("unknown component type: " .. component_type)
end
