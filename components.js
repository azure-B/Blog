/* ═══════════════════════════════════════════════════
   components.js — 사이드바 & 탑바 공통 컴포넌트
   모든 페이지에서 <script src="components.js"></script> 로 불러옵니다.
   (posts/ 하위 파일은 ../components.js)

   사용법:
     renderLayout({
       page: 'tech',           // 현재 페이지 키 (nav 활성화에 사용)
       breadcrumb: '기술 분석', // 탑바에 표시될 이름
       root: '../'              // posts/ 하위 파일이면 '../', 루트면 ''
     });
═══════════════════════════════════════════════════ */

function renderLayout({ page, breadcrumb, root = '' }) {
  const r = root;

  // ── CSS 동적 주입 (GitHub Pages 경로 문제 방지) ──
  // 기존 <link href="...common.css"> 를 제거하고 정확한 경로로 재주입합니다.
  document.querySelectorAll('link[rel="stylesheet"]').forEach(el => el.remove());
  const cssLink = document.createElement('link');
  cssLink.rel  = 'stylesheet';
  cssLink.href = `${r}common.css`;
  document.head.appendChild(cssLink);

  // ── 테마 초기화 (저장된 설정 또는 시스템 설정 따름) ──
  const savedTheme = localStorage.getItem('blog-theme');
  const preferLight = window.matchMedia('(prefers-color-scheme: light)').matches;
  if (savedTheme === 'light' || (!savedTheme && preferLight)) {
    document.documentElement.classList.add('light');
  }

  // ── 탑바 날짜 ──
  const now = new Date();
  const dateStr = `${now.getFullYear()}.${String(now.getMonth()+1).padStart(2,'0')}.${String(now.getDate()).padStart(2,'0')}`;

  // ── 네비게이션 메뉴 정의 ──
  const navItems = [
    { key: 'home',     icon: '⌂', label: '홈',         sub: 'HOME',              href: `${r}index.html` },
    { key: 'about',    icon: '◉', label: '소개',        sub: 'ABOUT',             href: `${r}about.html` },
    { type: 'section', label: '게시판' },
    { key: 'tech',     icon: '⎔', label: '기술 분석',   sub: 'TECH ANALYSIS',     href: `${r}tech.html` },
    { key: 'project',  icon: '◈', label: '프로젝트 리뷰', sub: 'PROJECT REVIEW',  href: `${r}project.html` },
    { key: 'external', icon: '◎', label: '대외 활동',   sub: 'EXTERNAL ACTIVITY', href: `${r}external.html` },
    { key: 'campus',   icon: '◐', label: '교내 활동',   sub: 'CAMPUS ACTIVITY',   href: `${r}campus.html` },
    { type: 'section', label: '기타' },
    { key: 'template', icon: '⊞', label: '글쓰기 템플릿', sub: 'TEMPLATE',        href: `${r}template.html` },
  ];

  const navHTML = navItems.map(item => {
    if (item.type === 'section') {
      return `<div class="nav-section-label">${item.label}</div>`;
    }
    const isActive = item.key === page ? 'active' : '';
    return `
      <a class="nav-item ${isActive}" href="${item.href}">
        <span class="nav-icon">${item.icon}</span>
        <div class="nav-text">
          <span class="nav-text-main">${item.label}</span>
          <span class="nav-text-sub">${item.sub}</span>
        </div>
      </a>`;
  }).join('');

  // ── 사이드바 HTML ──
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
          <span class="tag">곽노윤 교수</span>
          <span class="tag">구름톤 2025</span>
          <span class="tag">폴라리스</span>
        </div>
      </div>
      <nav class="sidebar-nav">${navHTML}</nav>
    </aside>`;

  // ── 탑바 HTML ──
  const topbarHTML = `
    <div class="topbar">
      <div class="topbar-breadcrumb">
        이승빈 <span>/</span> ${breadcrumb}
      </div>
      <div class="topbar-line"></div>
      <div class="topbar-meta">${dateStr}</div>
      <button class="theme-toggle" id="theme-toggle" title="다크/라이트 모드 전환" aria-label="테마 전환">
        ${document.documentElement.classList.contains('light') ? '🌙' : '☀️'}
      </button>
    </div>`;

  // ── 모바일 햄버거 버튼 & 오버레이 ──
  const mobHTML = `
    <button class="mob-menu-btn" id="mob-menu-btn" aria-label="메뉴 열기">
      <span></span><span></span><span></span>
    </button>
    <div class="mob-overlay" id="mob-overlay"></div>`;

  // ── #app 에 주입 ──
  const app = document.getElementById('app');
  app.innerHTML = sidebarHTML + `<main class="main">${topbarHTML}` + app.innerHTML + `</main>` + mobHTML;

  // ── 테마 토글 이벤트 ──
  const themeBtn = document.getElementById('theme-toggle');
  themeBtn.addEventListener('click', () => {
    const isLight = document.documentElement.classList.toggle('light');
    themeBtn.textContent = isLight ? '🌙' : '☀️';
    localStorage.setItem('blog-theme', isLight ? 'light' : 'dark');
  });

  // ── 햄버거 토글 동작 ──
  const btn     = document.getElementById('mob-menu-btn');
  const overlay = document.getElementById('mob-overlay');
  const sidebar = document.querySelector('.sidebar');

  function openMenu() {
    sidebar.classList.add('open');
    btn.classList.add('open');
    overlay.classList.add('visible');
    document.body.style.overflow = 'hidden';
  }
  function closeMenu() {
    sidebar.classList.remove('open');
    btn.classList.remove('open');
    overlay.classList.remove('visible');
    document.body.style.overflow = '';
  }

  btn.addEventListener('click', () => {
    sidebar.classList.contains('open') ? closeMenu() : openMenu();
  });
  overlay.addEventListener('click', closeMenu);

  // 사이드바 링크 클릭 시 모바일에서 메뉴 자동 닫기
  sidebar.querySelectorAll('a.nav-item').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 640) closeMenu();
    });
  });
}