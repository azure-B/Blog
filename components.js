/* ═══════════════════════════════════════════════════
   components.js
═══════════════════════════════════════════════════ */

function renderLayout({ page, breadcrumb, root = '' }) {
  const r = root;

  document.querySelectorAll('link[rel="stylesheet"]').forEach(el => el.remove());
  const cssLink = document.createElement('link');
  cssLink.rel  = 'stylesheet';
  cssLink.href = `${r}common.css`;
  document.head.appendChild(cssLink);

  /* ── KaTeX ── */
  function renderMath() {
    if (typeof renderMathInElement === 'undefined') return;
    document.querySelectorAll('.detail-content, .formula').forEach(el => {
      renderMathInElement(el, {
        delimiters: [
          { left: '$$',  right: '$$',  display: true  },
          { left: '\\[', right: '\\]', display: true  },
          { left: '$',   right: '$',   display: false },
          { left: '\\(', right: '\\)', display: false },
        ],
        throwOnError: false,
      });
    });
  }
  if (!document.getElementById('katex-css')) {
    const kCss = document.createElement('link');
    kCss.id = 'katex-css'; kCss.rel = 'stylesheet';
    kCss.href = 'https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css';
    document.head.appendChild(kCss);
    const kJs = document.createElement('script');
    kJs.src = 'https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js';
    kJs.onload = () => {
      const ar = document.createElement('script');
      ar.src = 'https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js';
      ar.onload = renderMath;
      document.head.appendChild(ar);
    };
    document.head.appendChild(kJs);
  } else {
    setTimeout(renderMath, 0);
  }

  /* ── 테마 초기화 ── */
  const savedTheme  = localStorage.getItem('blog-theme');
  const preferLight = window.matchMedia('(prefers-color-scheme: light)').matches;
  if (savedTheme === 'light' || (!savedTheme && preferLight)) {
    document.documentElement.classList.add('light');
  }

  /* ── 날짜 ── */
  const now = new Date();
  const dateStr = `${now.getFullYear()}.${String(now.getMonth()+1).padStart(2,'0')}.${String(now.getDate()).padStart(2,'0')}`;

  /* ── 게시글 카운트 ── */
  const pd = window.POSTS_DATA || {};
  const counts = {
    tech:     (pd.tech     || []).length,
    project:  (pd.project  || []).length,
    external: (pd.external || []).length,
    campus:   (pd.campus   || []).length,
  };
  const totalCount = Object.values(counts).reduce((s, n) => s + n, 0);

  /* ── 네비게이션 ── */
  const navItems = [
    { key: 'home',     icon: '⌂', label: '홈',           sub: 'HOME',              href: `${r}index.html` },
    { key: 'about',    icon: '◉', label: '소개',          sub: 'ABOUT',             href: `${r}about.html` },
    { type: 'section', label: '게시판' },
    { key: 'tech',     icon: '⎔', label: '기술 분석',     sub: 'TECH ANALYSIS',     href: `${r}tech.html`,     count: counts.tech },
    { key: 'project',  icon: '◈', label: '프로젝트 리뷰', sub: 'PROJECT REVIEW',    href: `${r}project.html`,  count: counts.project },
    { key: 'external', icon: '◎', label: '대외 활동',     sub: 'EXTERNAL ACTIVITY', href: `${r}external.html`, count: counts.external },
    { key: 'campus',   icon: '◐', label: '교내 활동',     sub: 'CAMPUS ACTIVITY',   href: `${r}campus.html`,   count: counts.campus },
    { type: 'section', label: '기타' },
    { key: 'template', icon: '⊞', label: '글쓰기 템플릿', sub: 'TEMPLATE',          href: `${r}template.html` },
  ];

  const navHTML = navItems.map(item => {
    if (item.type === 'section') return `<div class="nav-section-label">${item.label}</div>`;
    const isActive = item.key === page ? 'active' : '';
    const countBadge = item.count != null
      ? `<span class="nav-count">${item.count}</span>`
      : '';
    return `
      <a class="nav-item ${isActive}" href="${item.href}">
        <span class="nav-icon">${item.icon}</span>
        <div class="nav-text">
          <span class="nav-text-main">${item.label}</span>
          <span class="nav-text-sub">${item.sub}</span>
        </div>
        ${countBadge}
      </a>`;
  }).join('');

  /* ── 총 게시글 수 ── */
  const totalBadge = totalCount > 0
    ? `<div class="profile-post-count">
         <span class="profile-post-num">${totalCount}</span>
         <span class="profile-post-label">POSTS</span>
       </div>`
    : '';

  /* ── HTML 조립 ── */
  const sidebarHTML = `
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="site-label">Portfolio &amp; Dev Blog</div>
        <a class="site-name" href="${r}index.html" style="text-decoration:none;">이승<span>빈</span></a>
      </div>
      <div class="profile-card">
        <div class="profile-avatar">SB</div>
        <div class="profile-name">이승빈</div>
        <div class="profile-role">// IPCG Lab Leader</div>
        <div class="profile-tags">
          <span class="tag accent">백석대학교</span>
          <span class="tag">구름톤 2025</span>
          <span class="tag">폴라리스</span>
        </div>
        ${totalBadge}
      </div>
      <nav class="sidebar-nav">${navHTML}</nav>
    </aside>`;

  const topbarHTML = `
    <div class="topbar">
      <div class="topbar-breadcrumb">이승빈 <span>/</span> ${breadcrumb}</div>
      <div class="topbar-line"></div>
      <div class="topbar-meta">${dateStr}</div>
      <button class="theme-toggle" id="theme-toggle" title="다크/라이트 모드 전환" aria-label="테마 전환">
        ${document.documentElement.classList.contains('light') ? '🌙' : '☀️'}
      </button>
    </div>`;

  const mobHTML = `
    <button class="mob-menu-btn" id="mob-menu-btn" aria-label="메뉴 열기">
      <span></span><span></span><span></span>
    </button>
    <div class="mob-overlay" id="mob-overlay"></div>`;

  const app = document.getElementById('app');
  app.innerHTML = sidebarHTML + `<main class="main">${topbarHTML}` + app.innerHTML + `</main>` + mobHTML;

  /* ── 테마 토글 ── */
  const themeBtn = document.getElementById('theme-toggle');
  themeBtn.addEventListener('click', () => {
    const isLight = document.documentElement.classList.toggle('light');
    themeBtn.textContent = isLight ? '🌙' : '☀️';
    localStorage.setItem('blog-theme', isLight ? 'light' : 'dark');
  });

  /* ── 햄버거 ── */
  const btn     = document.getElementById('mob-menu-btn');
  const overlay = document.getElementById('mob-overlay');
  const sidebar = document.querySelector('.sidebar');

  function openMenu()  { sidebar.classList.add('open'); btn.classList.add('open'); overlay.classList.add('visible'); document.body.style.overflow = 'hidden'; }
  function closeMenu() { sidebar.classList.remove('open'); btn.classList.remove('open'); overlay.classList.remove('visible'); document.body.style.overflow = ''; }

  btn.addEventListener('click', () => sidebar.classList.contains('open') ? closeMenu() : openMenu());
  overlay.addEventListener('click', closeMenu);
  sidebar.querySelectorAll('a.nav-item').forEach(link => {
    link.addEventListener('click', () => { if (window.innerWidth <= 640) closeMenu(); });
  });

  /* ── TOC ── */
  const content = document.querySelector('.detail-content');
  if (!content) return;

  const headings = [...content.querySelectorAll('h2, h3, h4')];
  if (headings.length < 2) return;

  headings.forEach((h, i) => { if (!h.id) h.id = 'toc-' + i; });

  const toc = document.createElement('nav');
  toc.className = 'toc';
  toc.innerHTML = '<div class="toc-label">목차</div>';
  const ul = document.createElement('ul');
  ul.className = 'toc-list';

  headings.forEach(h => {
    const depth = parseInt(h.tagName[1]);
    const li = document.createElement('li');
    li.className = `toc-item depth-${depth}`;
    const a = document.createElement('a');
    a.className = 'toc-link';
    a.href = '#' + h.id;
    a.textContent = h.textContent.replace(/[↗→]/g, '').trim();
    a.addEventListener('click', e => {
      e.preventDefault();
      const top = h.getBoundingClientRect().top + window.scrollY - 72;
      window.scrollTo({ top, behavior: 'smooth' });
      history.pushState(null, '', '#' + h.id);
    });
    li.appendChild(a);
    ul.appendChild(li);
  });

  toc.appendChild(ul);
  document.body.appendChild(toc);

  function checkWidth() { toc.classList.toggle('visible', window.innerWidth >= 1300); }
  checkWidth();
  window.addEventListener('resize', checkWidth);

  const links = [...toc.querySelectorAll('.toc-link')];
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        links.forEach(l => l.classList.remove('active'));
        const active = links.find(l => l.getAttribute('href') === '#' + entry.target.id);
        if (active) active.classList.add('active');
      }
    });
  }, { rootMargin: '-10% 0px -80% 0px', threshold: 0 });

  headings.forEach(h => observer.observe(h));
}