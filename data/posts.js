/* ═══════════════════════════════════════════════════
   data/posts.js — 전체 게시글 목록
   
   새 글을 쓸 때:
     1. posts/{게시판}/{id}.html 파일 작성
     2. 아래 해당 배열에 객체 한 줄 추가
     3. 끝 — 게시판 페이지는 건드릴 필요 없음
═══════════════════════════════════════════════════ */

window.POSTS_DATA = {

  /* ── 기술 분석 ── */
  tech: [
    {
      id: 'tech-016',
      category: 'Algorithm',
      title: '정렬 알고리즘',
      excerpt: '선택 / 버블 / 삽입 정렬부터 퀵정렬까지.',
      tags: ['Algorithm'],
      date: '2026.04.18',
    },  
    {
      id: 'tech-015',
      category: 'Algorithm',
      title: '점화식 / 반복 대치, 마스터 정리',
      excerpt: '점화식 / 반복 대치, 마스터 정리에 대해 알아보았다.',
      tags: ['Algorithm'],
      date: '2026.04.17',
    },
      {
      id: 'tech-014',
      category: 'Algorithm',
      title: '시간 복잡도 / 점근적 표기법',
      excerpt: '시간 복잡도 / 점근적 표기법에 대해 알아보았다.',
      tags: ['Algorithm'],
      date: '2026.04.16',
    },
    {
      id: 'tech-013',
      category: 'Algorithm',
      title: 'Algorithm',
      excerpt: 'Algorithm이란 무엇인가?',
      tags: ['Algorithm'],
      date: '2026.04.16',
    },
    {
      id: 'tech-012',
      category: 'Data Structure',
      title: 'Data Structure - Stack, Queue, Tree',
      excerpt: '스택과 큐, 트리',
      tags: ['Data Structure'],
      date: '2026.04.16',
    },
    {
      id: 'tech-011',
      category: 'Deep Learning',
      title: 'Mini-Batch Gradient Descent',
      excerpt: 'GAN에서 나오는 Mini-Batch Gradient Descent에 대해 알아보았습니다.',
      tags: ['Keras', 'TensorFlow'],
      date: '2026.04.10',
    },
    {
      id: 'tech-010',
      category: 'Deep Learning',
      title: 'Jensen-Shannon Divergence',
      excerpt: 'GAN에서 나오는 Jensen-Shannon Divergence에 대해 알아보았습니다.',
      tags: ['Keras', 'TensorFlow'],
      date: '2026.04.07',
    },
    {
      id: 'tech-009',
      category: 'Deep Learning',
      title: 'tf.keras.layers.Layer',
      excerpt: 'tf.keras.layers.Layer에 대해 심도있게 다루어 보았습니다.',
      tags: ['Keras', 'TensorFlow'],
      date: '2026.04.07',
    },
    {
      id: 'tech-008',
      category: 'Deep Learning',
      title: 'KL Divergence',
      excerpt: 'GAN에서 나오는 KL Divergence에 대해 알아보았습니다.',
      tags: ['Deep Learning'],
      date: '2026.04.09',
    },
    {
      id: 'tech-007',
      category: 'Deep Learning',
      title: '교차 엔트로피와 최대 우도 추정',
      excerpt: '적대적 프레임워크의 수학적 공식에서 Log를 쓰는 이유를 모르기에 알아보았습니다.',
      tags: ['Deep Learning'],
      date: '2026.04.02',
    },
    {
      id: 'tech-006',
      category: 'Deep Learning',
      title: '생성적 적대 신경망에 대하여',
      excerpt: '역전파와 드롭아웃만을 사용하여 발생시킨 혁신.',
      tags: ['Deep Learning'],
      date: '2026.03.31',
    },
    {
      id: 'tech-005',
      category: 'Deep Learning',
      title: 'RELU에 대하여',
      excerpt: '항상 신경망을 구성할 때 사용한 활성화 함수인 RELU에 대해 알아보았습니다.',
      tags: ['Deep Learning'],
      date: '2026.03.30',
    },
    {
      id: 'tech-004',
      category: 'TensorFlow',
      title: 'Tensor 자료구조',
      excerpt: 'TensorFlow를 공부하고 있으나, 정작 Tensor에 대해 아는 것은 없는 것 같아 처음부터 공부해보려고 합니다.',
      tags: ['TensorFlow'],
      date: '2026.03.27',
    },
    {
      id: 'tech-003',
      category: 'Transformer',
      title: 'Self-Attention 메커니즘 수식 완전 분해',
      excerpt: 'Query, Key, Value의 역할과 Scaled Dot-Product Attention을 수식부터 코드까지 단계별로 분석합니다.',
      tags: ['Deep Learning'],
      date: '2025.07.01',
    },
    {
      id: 'tech-002',
      category: 'Deep Learning',
      title: 'CNN(합성곱 신경망) 구조 분석 — 필터부터 풀링까지',
      excerpt: '합성곱 연산, 패딩, 스트라이드, 풀링의 작동 방식을 직접 계산 예시와 함께 정리합니다.',
      tags: ['Deep Learning'],
      date: '2025.06.20',
    },
    {
      id: 'tech-001',
      category: 'Machine Learning',
      title: '로지스틱 회귀(Logistic Regression) 완전 분석',
      excerpt: '시그모이드 함수부터 최대 우도 추정, 경사하강법까지 로지스틱 회귀의 수학적 기반을 정리했습니다.',
      tags: ['Deep Learning'],
      date: '2025.06.10',
    },
  ],

  /* ── 프로젝트 리뷰 ── */
  project: [
    {
      id: 'project-002',
      category: 'Deep Learning',
      title: 'DeepFake Scanner',
      excerpt: '딥러닝에 공부하기 위해 파인 튜닝이 아닌 처음부터 전체 파이프라인을 설계하였습니다.',
      tags: ['Deep Learning', 'TensorFlow', 'MediaPipe'],
      date: '2025.04.20',
    },
    {
      id: 'project-001',
      category: 'LLM',
      title: '멍멍케어',
      excerpt: 'PyTorch로 Exaone3.5를 파인튜닝하여 어플리케이션을 만든 프로젝트입니다.',
      tags: ['Exaone3.5', 'Pytorch'],
      date: '2025.11.15',
    },
  ],

  /* ── 대외 활동 ── */
  external: [
    {
      id: 'external-002',
      category: 'AI 대회',
      title: '공개 AI 경진대회 참가기 — 이미지 분류 태스크',
      excerpt: 'Dacon 이미지 분류 대회에 처음 참가했습니다. EfficientNet 파인튜닝부터 앙상블까지 전 과정을 공유합니다.',
      tags: ['Dacon', 'EfficientNet', 'Image Classification', '대회'],
      date: '2025.06.01',
    },
    {
      id: 'external-001',
      category: '해커톤',
      title: '구름톤 2025 유니브 부대표 활동 회고',
      excerpt: '전국 대학생 개발자 연합 해커톤 구름톤 유니브에서 부대표로 활동한 6개월의 여정을 기록합니다.',
      tags: ['9oormthon', '구름톤', '해커톤', '운영진'],
      date: '2025.07.10',
    },
  ],

  /* ── 교내 활동 ── */
  campus: [
     {
      id: 'campus-006',
      category: 'DeepLearning Programming',
      title: 'DeepLearning Programming - Open Book Test - 3',
      excerpt: 'DeepLearning Programming 교과의 Open Book test를 위한 정리본',
      tags: ['DeepLearning Programming'],
      date: '2026.04.01',
    },
    {
      id: 'campus-004',
      category: 'DeepLearning Programming',
      title: 'DeepLearning Programming - Open Book Test - 2',
      excerpt: 'DeepLearning Programming 교과의 Open Book test를 위한 정리본',
      tags: ['DeepLearning Programming'],
      date: '2026.04.01',
    },
    {
      id: 'campus-005',
      category: 'DeepLearning Programming',
      title: 'DeepLearning Programming - Open Book Test',
      excerpt: 'DeepLearning Programming 교과의 Open Book test를 위한 정리본',
      tags: ['DeepLearning Programming'],
      date: '2026.04.01',
    },
    {
      id: 'campus-003',
      category: 'IPCG Lab',
      title: 'IPCG 랩 정기 세미나 — seq to seq',
      excerpt: '랩 세미나에서 케라스 창시자에게 배우는 딥러닝의 transformer architecture 파트의 일부를 발표하였습니다.',
      tags: ['IPCG Lab', 'Tensorflow', 'Lab Seminar'],
      date: '2026.04.01',
    },
    {
      id: 'campus-002',
      category: 'IPCG Lab',
      title: 'IPCG 랩 정기 세미나 — Self Attention',
      excerpt: '랩 세미나에서 케라스 창시자에게 배우는 딥러닝의 transformer architecture 파트의 일부를 발표하였습니다.',
      tags: ['IPCG Lab', 'Tensorflow', 'Lab Seminar'],
      date: '2026.03.25',
    },
    {
      id: 'campus-001',
      category: 'IPCG Lab',
      title: 'IPCG 랩 정기 세미나 — Transformer',
      excerpt: '랩 세미나에서 케라스 창시자에게 배우는 딥러닝의 transformer architecture 파트의 일부를 발표하였습니다.',
      tags: ['IPCG Lab', 'Tensorflow', 'Lab Seminar'],
      date: '2026.03.24',
    },
  ],

};