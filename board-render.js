/* ═══════════════════════════════════════════════════
   board-render.js
   
   사용법: initBoard(posts, board)
     posts — window.POSTS_DATA.tech 등
     board — 'tech' | 'campus' | 'project' | 'external'
═══════════════════════════════════════════════════ */

function initBoard(posts, board) {
  const listEl = document.getElementById('post-list');

  let searchQuery    = '';
  let activeCategory = '';
  let activeTag      = '';

  const categories = [...new Set(posts.map(p => p.category).filter(Boolean))];
  const allTags    = [...new Set(posts.flatMap(p => p.tags || []))];

  const boardHeader = document.querySelector('.board-header');

  const searchWrap = document.createElement('div');
  searchWrap.className = 'board-search-wrap';
  searchWrap.innerHTML = `
    <div class="board-search-box">
      <span class="board-search-icon">🔍</span>
      <input class="board-search-input" id="search-input" type="text"
        placeholder="제목, 내용, 태그 검색..." autocomplete="off" spellcheck="false" />
      <button class="board-search-clear" id="search-clear" title="검색어 지우기">✕</button>
    </div>`;
  boardHeader.after(searchWrap);

  const filterRow = document.createElement('div');
  filterRow.className = 'board-filter-row';
  filterRow.id = 'filter-row';
  searchWrap.after(filterRow);

  renderFilters();

  const searchInput = document.getElementById('search-input');
  const searchClear = document.getElementById('search-clear');

  searchInput.addEventListener('input', () => {
    searchQuery = searchInput.value.trim();
    searchClear.classList.toggle('visible', searchQuery.length > 0);
    render();
  });
  searchClear.addEventListener('click', () => {
    searchInput.value = '';
    searchQuery = '';
    searchClear.classList.remove('visible');
    searchInput.focus();
    render();
  });

  function renderFilters() {
    const row = document.getElementById('filter-row');
    if (!row) return;
    const showCats = categories.length > 1;
    const showTags = allTags.length > 0;
    if (!showCats && !showTags) { row.style.display = 'none'; return; }

    let html = '';
    if (showCats) {
      html += `<span class="filter-label">카테고리</span>`;
      html += `<button class="filter-pill ${activeCategory === '' ? 'active' : ''}" data-cat="">전체</button>`;
      categories.forEach(cat => {
        html += `<button class="filter-pill ${activeCategory === cat ? 'active' : ''}" data-cat="${esc(cat)}">${esc(cat)}</button>`;
      });
    }
    if (showCats && showTags) html += `<span class="filter-sep"></span>`;
    if (showTags) {
      html += `<span class="filter-label">태그</span>`;
      allTags.forEach(tag => {
        html += `<button class="filter-pill ${activeTag === tag ? 'active' : ''}" data-tag="${esc(tag)}">#${esc(tag)}</button>`;
      });
    }
    row.innerHTML = html;

    row.querySelectorAll('[data-cat]').forEach(btn => {
      btn.addEventListener('click', () => { activeCategory = btn.dataset.cat; activeTag = ''; renderFilters(); render(); });
    });
    row.querySelectorAll('[data-tag]').forEach(btn => {
      btn.addEventListener('click', () => { activeTag = activeTag === btn.dataset.tag ? '' : btn.dataset.tag; activeCategory = ''; renderFilters(); render(); });
    });
  }

  function render() {
    const q = searchQuery.toLowerCase();
    const filtered = posts.filter(p => {
      const matchCat = !activeCategory || p.category === activeCategory;
      const matchTag = !activeTag      || (p.tags || []).includes(activeTag);
      const matchQ   = !q ||
        p.title.toLowerCase().includes(q) ||
        (p.excerpt || '').toLowerCase().includes(q) ||
        (p.category || '').toLowerCase().includes(q) ||
        (p.tags || []).some(t => t.toLowerCase().includes(q));
      return matchCat && matchTag && matchQ;
    });

    if (filtered.length === 0) {
      listEl.innerHTML = `<div class="post-empty">검색 결과가 없습니다.</div>`;
      return;
    }

    listEl.innerHTML = filtered.map((p, i) => {
      const tagsHtml = (p.tags || []).map(t => {
        const isMatch = (activeTag === t) || (q && t.toLowerCase().includes(q));
        return `<span class="post-tag ${isMatch ? 'matched' : ''}">#${esc(t)}</span>`;
      }).join('');

      return `
        <a class="post-item" href="posts/${board}/${p.id}.html">
          <div class="post-num">0${filtered.length - i}</div>
          <div class="post-body">
            <span class="post-cat">${esc(p.category)}</span>
            <div class="post-title">${highlight(p.title, q)}</div>
            <div class="post-excerpt">${highlight(p.excerpt || '', q)}</div>
            <div class="post-tags">${tagsHtml}</div>
          </div>
          <div class="post-meta">
            <div class="post-date">${p.date}</div>
          </div>
        </a>`;
    }).join('');
  }

  function esc(str) {
    return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
  function highlight(text, q) {
    if (!q) return esc(text);
    return esc(text).replace(new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')})`, 'gi'), '<mark class="search-highlight">$1</mark>');
  }

  render();
}