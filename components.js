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
  const r = root; // 경로 접두사

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
        <div class="profile-avatar">Azure</div>
        <div class="profile-name">이승빈</div>
        <div class="profile-role">// IPCG Lab Leader</div>
        <div class="profile-tags">
          <span class="tag accent">백석대학교</span>
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
    </div>`;

  // ── #app 에 주입 ──
  const app = document.getElementById('app');
  app.innerHTML = sidebarHTML + `<main class="main">${topbarHTML}` + app.innerHTML + `</main>`;
}
