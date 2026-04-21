# =============================================================================
#  XOR / 다층신경망 / TensorBoard / Cost함수 / Queue Runner 완전 정복
#  (실행용 아님 - AI 없이 직접 코드 작성 시 참고하기 위한 완벽 레퍼런스 가이드)
# =============================================================================
#
#  목차
#  [1]  XOR 문제란 — 왜 단층으로 못 푸나
#  [2]  lab-09-1  단층 퍼셉트론 XOR (실패 케이스)
#  [3]  lab-09-2  다층 신경망 XOR   (성공 케이스)
#  [4]  성능 차이가 발생하는 이유
#  [5]  TensorBoard (lab-09-4) — 전체 동작 과정
#  [6]  Cost 함수 완전 정리 (선형회귀 / 이진분류 / 다중분류)
#  [7]  전체 선언 패턴 요약
#  [8]  [추가] Queue Runner — 대용량 데이터 파이프라인
# =============================================================================

import tensorflow as tf
import numpy as np
tf.set_random_seed(777)


# =============================================================================
# [1]  XOR 문제란 — 왜 단층으로 못 푸나
# =============================================================================
#
#  XOR 진리표
#  ┌───┬───┬────────┐
#  │ X1│ X2│ Y(XOR) │
#  ├───┼───┼────────┤
#  │ 0 │ 0 │   0    │
#  │ 0 │ 1 │   1    │
#  │ 1 │ 0 │   1    │
#  │ 1 │ 1 │   0    │
#  └───┴───┴────────┘
#
#  XOR은 선형 분리 불가능(Linearly Non-Separable) 문제다.
#  직선 하나로 0과 1을 구분할 수 없음.
#
#  좌표로 표시하면:
#  (0,0)→0  (1,1)→0  : 직선 아래
#  (0,1)→1  (1,0)→1  : 직선 위
#  → 어떻게 직선을 그어도 한 번에 분리 불가
#
#  단층 퍼셉트론(W 하나, b 하나)은
#  결국 직선 하나를 학습하는 것과 같음
#  → XOR을 직선으로 분리할 수 없으므로 단층으로는 절대 못 품
#  → 정확도가 0.5(찍는 수준)에 머무름


# =============================================================================
# [2]  lab-09-1  단층 퍼셉트론 XOR — 왜 이렇게 쓰는가 (실패 케이스)
# =============================================================================

x_data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)
y_data = np.array([[0],     [1],    [1],    [0]],    dtype=np.float32)
# XOR의 4가지 입력·정답 쌍을 전부 넣음
# dtype=np.float32 : TF Variable이 float32이므로 맞춰야 feed_dict 에러 없음

X = tf.placeholder(tf.float32, [None, 2])   # 입력 피처 2개 (X1, X2)
Y = tf.placeholder(tf.float32, [None, 1])   # 출력 1개 (0 또는 1)

# ── 단층 구조 : W 하나, b 하나 ──────────────────────────────────────────
W = tf.Variable(tf.random_normal([2, 1]), name="weight")
b = tf.Variable(tf.random_normal([1]),    name="bias")
# W : (2,1) → X(N,2) @ W(2,1) = (N,1)  출력 1개짜리 선형 경계선

hypothesis = tf.sigmoid(tf.matmul(X, W) + b)
# sigmoid : 0~1 사이 확률값으로 변환 → 0.5 기준으로 0/1 분류

cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) * tf.log(1 - hypothesis))
# Binary Cross-Entropy : 이진 분류의 표준 손실함수

train = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)

predicted = tf.cast(hypothesis > 0.5, dtype=tf.float32)
accuracy  = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32))

# ── 실행 결과 ─────────────────────────────────────────────────────────────
# Hypothesis : [[0.5] [0.5] [0.5] [0.5]]  ← 모든 입력에 대해 0.5 출력
# Correct    : [[0.]  [0.]  [0.]  [0.]]   ← 전부 0으로 예측
# Accuracy   : 0.5                         ← 찍는 수준
#
# [해석]
# 아무리 학습해도 cost가 더 이상 줄어들지 않음 (수렴했지만 틀린 상태)
# 단층으로는 XOR의 비선형 경계를 표현할 수 없기 때문


# =============================================================================
# [3]  lab-09-2  다층 신경망 XOR — 왜 이렇게 쓰는가 (성공 케이스)
# =============================================================================
#
#  구조 : 입력(2) → 은닉층(2뉴런, sigmoid) → 출력(1뉴런, sigmoid)
#  핵심 : 은닉층이 비선형 변환을 수행해서 XOR도 분리 가능하게 만들어줌

X2 = tf.placeholder(tf.float32, [None, 2])
Y2 = tf.placeholder(tf.float32, [None, 1])

# ── Layer 1 : 입력(2) → 은닉(2) ─────────────────────────────────────────
W1 = tf.Variable(tf.random_normal([2, 2]), name="weight1")
b1 = tf.Variable(tf.random_normal([2]),    name="bias1")
layer1 = tf.sigmoid(tf.matmul(X2, W1) + b1)
# W1 : (2,2)  →  X(N,2) @ W1(2,2) = (N,2)
# 은닉층 뉴런 수(2)는 설계자가 결정 (2~수백)
# sigmoid : 비선형 활성화 → 이 비선형성이 XOR 풀이의 핵심

# ── Layer 2 : 은닉(2) → 출력(1) ─────────────────────────────────────────
W2 = tf.Variable(tf.random_normal([2, 1]), name="weight2")
b2 = tf.Variable(tf.random_normal([1]),    name="bias2")
hypothesis2 = tf.sigmoid(tf.matmul(layer1, W2) + b2)
# layer1(N,2) @ W2(2,1) = (N,1)  →  최종 이진 분류 출력

cost2  = -tf.reduce_mean(Y2 * tf.log(hypothesis2) + (1 - Y2) * tf.log(1 - hypothesis2))
train2 = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost2)

predicted2 = tf.cast(hypothesis2 > 0.5, dtype=tf.float32)
accuracy2  = tf.reduce_mean(tf.cast(tf.equal(predicted2, Y2), dtype=tf.float32))

# ── 실행 결과 ─────────────────────────────────────────────────────────────
# Hypothesis : [[0.01] [0.98] [0.98] [0.01]]  ← 정답에 근접한 확률
# Correct    : [[0.]   [1.]   [1.]   [0.]]    ← 전부 올바르게 예측
# Accuracy   : 1.0                             ← 완벽한 분류
#
# [해석]
# 은닉층의 sigmoid가 입력 공간을 비선형 변환 → XOR 분리 가능한 형태로 바꿈
# Layer1이 (0,0)/(1,1) 과 (0,1)/(1,0)을 구분할 수 있는 특징을 학습


# =============================================================================
# [4]  성능 차이가 발생하는 이유
# =============================================================================
#
#  단층(lab-09-1) vs 다층(lab-09-2) 비교
#  ┌──────────────┬──────────────────────┬──────────────────────┐
#  │              │ lab-09-1 (단층)      │ lab-09-2 (다층)      │
#  ├──────────────┼──────────────────────┼──────────────────────┤
#  │ 구조         │ 입력→출력 (직결)     │ 입력→은닉→출력       │
#  │ W 개수       │ 1개 (2×1)            │ 2개 (2×2, 2×1)       │
#  │ 결정 경계    │ 직선 1개             │ 곡선/복잡한 경계 가능 │
#  │ cost(마지막) │ ~0.69 (수렴 실패)    │ ~0.001 (정상 수렴)   │
#  │ Accuracy     │ 0.5 (찍는 수준)      │ 1.0 (완벽)           │
#  └──────────────┴──────────────────────┴──────────────────────┘
#
#  핵심 이유 : 표현력(Representational Power)의 차이
#
#  단층 = 선형 변환 + sigmoid
#       = 결국 하나의 선형 경계만 표현 가능
#       → XOR처럼 비선형인 문제는 풀 수 없음 (1969년 Minsky & Papert 증명)
#
#  다층 = 여러 선형 변환 + 비선형 활성화 함수의 조합
#       = 임의의 복잡한 함수를 근사 가능 (Universal Approximation Theorem)
#       → 은닉층이 입력 공간을 비선형으로 변환해서 선형 분리 가능한 형태로 만듦
#
#  쉽게 말하면:
#  Layer1이 "(0,0)/(1,1) = 비슷한 그룹" vs "(0,1)/(1,0) = 비슷한 그룹" 으로
#  공간을 재배치하고, Layer2가 그 위에서 직선으로 분류하는 방식


# =============================================================================
# [5]  TensorBoard (lab-09-4) — 전체 동작 과정
# =============================================================================
#
#  TensorBoard란?
#  TensorFlow에서 제공하는 시각화 도구
#  학습 과정(loss, accuracy), 모델 구조(그래프), 가중치 분포를 웹 UI로 확인 가능
#  딥러닝 디버깅 및 하이퍼파라미터 튜닝에 필수
#
#  ── [5-1] name_scope : 그래프 그룹화 ──────────────────────────────────
#
#  with tf.name_scope("Layer1"):
#      W1 = tf.Variable(...)
#      b1 = tf.Variable(...)
#      layer1 = tf.sigmoid(...)
#
#  · name_scope는 TensorBoard 그래프 시각화에서 관련 노드를 묶어줌
#  · "Layer1" 이라는 블록으로 그룹화되어 복잡한 그래프를 깔끔하게 볼 수 있음
#  · 실제 연산에는 영향 없음 — 시각화 용도


#  ── [5-2] summary : 학습 중 기록할 데이터 지정 ─────────────────────────
#
#  tf.summary.histogram("W1", W1)
#  → W1의 값 분포(히스토그램)를 기록  (가중치가 어떻게 변하는지 확인)
#
#  tf.summary.histogram("b1", b1)
#  → b1의 값 분포 기록
#
#  tf.summary.histogram("Layer1", layer1)
#  → Layer1 출력값의 분포 기록  (활성화 분포 확인)
#
#  tf.summary.scalar("Cost", cost)
#  → 스칼라 값(cost) 하나를 기록  (그래프로 추이 확인)
#
#  tf.summary.scalar("accuracy", accuracy)
#  → 정확도 추이 기록
#
#  histogram : 분포 확인용 (벡터/행렬 값 → 히스토그램)
#  scalar    : 추이 확인용 (숫자 1개 → 꺾은선 그래프)


#  ── [5-3] merge_all & FileWriter ───────────────────────────────────────
#
#  merged_summary = tf.summary.merge_all()
#  → 위에서 선언한 모든 summary를 하나로 합침
#  → sess.run할 때 한 번에 모든 summary를 계산하기 위해 필요
#
#  writer = tf.summary.FileWriter("./logs/xor_logs_r0_01")
#  → summary 데이터를 저장할 디렉토리 지정
#  → 이 폴더 안에 TensorBoard가 읽을 수 있는 이벤트 파일 생성됨
#
#  writer.add_graph(sess.graph)
#  → 모델의 연산 그래프를 TensorBoard에 추가
#  → TensorBoard의 GRAPHS 탭에서 시각화 가능


#  ── [5-4] Session 내 실행 패턴 ─────────────────────────────────────────
#
#  for step in range(10001):
#      _, summary, cost_val = sess.run(
#          [train, merged_summary, cost],
#          feed_dict={X: x_data, Y: y_data}
#      )
#      writer.add_summary(summary, global_step=step)
#
#  · merged_summary를 train과 함께 sess.run에 포함시켜야 매 스텝 기록됨
#  · writer.add_summary(summary, global_step=step) : step 번호와 함께 저장
#    → TensorBoard x축이 step 번호가 됨
#  · feed_dict 없음 → iterator 방식이 아닌 경우 feed_dict 필요


#  ── [5-5] TensorBoard 실행 방법 ────────────────────────────────────────
#
#  터미널에서:
#    tensorboard --logdir=./logs/xor_logs_r0_01
#
#  → 브라우저에서 http://localhost:6006 접속
#
#  폴더 여러 개 비교할 때 (하이퍼파라미터 비교):
#    tensorboard --logdir=./logs
#    (하위 폴더들을 자동으로 각각 다른 색으로 표시)


#  ── [5-6] TensorBoard 탭별 활용 ─────────────────────────────────────────
#
#  SCALARS  : cost, accuracy 등 스칼라 값의 학습 추이 그래프
#             → 과적합(train↑ val↓) 여부 확인, 수렴 속도 비교
#
#  GRAPHS   : 연산 그래프 구조 시각화 (name_scope로 묶인 그룹 확인)
#             → 모델 구조가 의도한 대로인지 디버깅
#
#  HISTOGRAMS : W, b 등의 값 분포 변화 (학습이 진행됨에 따라)
#             → 가중치가 제대로 학습되는지, Dead Neuron 있는지 확인
#
#  활용 방안 정리:
#  1) 학습률(learning_rate) 튜닝 : 다른 lr로 실험하고 cost 추이 비교
#  2) 모델 구조 디버깅 : 의도한 레이어 연결이 맞는지 GRAPHS에서 확인
#  3) 과적합 감지 : train/validation loss를 같이 기록해서 비교
#  4) 가중치 분포 이상 감지 : 특정 레이어 가중치가 0에 몰리면 dead neuron


# =============================================================================
# [6]  Cost 함수 완전 정리
# =============================================================================

#  ── (A) 선형 회귀 → MSE ────────────────────────────────────────────────
#
#  언제? : 출력이 연속 실수값 (집값, 온도, 점수 등)
#  출력층 : 활성화함수 없음 (그냥 선형)
#
#  hypothesis = tf.matmul(X, W) + b           # 출력 : -∞ ~ +∞
#  cost = tf.reduce_mean(tf.square(hypothesis - Y))
#
#  · tf.square : (예측 - 정답)²   음수든 양수든 항상 양수
#  · 큰 오차에 더 큰 패널티 (제곱이므로)
#  · reduce_mean : 전체 평균 → 스칼라

#  ── (B) 이진 분류 → BCE (Binary Cross-Entropy) ─────────────────────────
#
#  언제? : 출력이 0 또는 1 (생존/사망, 합격/불합격)
#  출력층 : sigmoid (0~1 확률값 출력)
#
#  hypothesis = tf.sigmoid(tf.matmul(X, W) + b)   # 출력 : 0 ~ 1
#  cost = -tf.reduce_mean(
#      Y * tf.log(hypothesis) + (1 - Y) * tf.log(1 - hypothesis)
#  )
#
#  · Y=1 : -log(hypothesis)   → h가 1에 가까울수록 cost ↓
#  · Y=0 : -log(1-hypothesis) → h가 0에 가까울수록 cost ↓
#  · 앞의 - : log는 음수이므로 양수로 만들기 위해 필수
#  · MSE 안 쓰는 이유 : sigmoid + MSE는 기울기 소실로 학습 느림

#  ── (C) 다중 분류 → CCE (Categorical Cross-Entropy) ────────────────────
#
#  언제? : 출력이 3개 이상 클래스 (MNIST 0~9, 감정 분류 등)
#  출력층 : softmax (클래스별 확률, 합=1)
#  Y 형태 : one-hot 인코딩  ex) 클래스2 → [0, 0, 1, 0, ...]
#
#  hypothesis = tf.nn.softmax(tf.matmul(X, W) + b)    # 출력 : (N, K)
#  cost = -tf.reduce_mean(
#      tf.reduce_sum(Y_onehot * tf.log(hypothesis + 1e-8), axis=1)
#  )
#
#  · Y_onehot * tf.log(hypothesis) : one-hot이므로 정답 클래스만 살아남
#  · tf.reduce_sum(axis=1) : 클래스 방향 합산 → 각 샘플별 loss (N,)
#    ← 이 axis=1이 CCE에만 있는 핵심 포인트
#  · tf.reduce_mean : 샘플 평균 → 스칼라
#  · +1e-8 : log(0) = -inf 방지 (수치 안정성)

#  ── (D) MNIST 방식 — reduce_sum 없이 쓰는 버전 ─────────────────────────
#
#  cost = -tf.reduce_mean(labels_onehot * tf.log(hypothesis + 1e-8))
#
#  · reduce_sum(axis=1) 없이 바로 reduce_mean 해도 결과가 비슷함
#  · 이유 : one-hot이므로 각 행에서 0이 아닌 값이 1개뿐
#           → 0들은 기여도가 0이라 평균에 거의 영향 없음
#  · 더 엄밀한 표준 CCE : reduce_sum(axis=1) 포함 버전


# =============================================================================
# [7]  전체 선언 패턴 요약 (경우의 수 모두)
# =============================================================================
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 문제 유형    출력층         Y 형태       Cost
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 선형 회귀   없음(선형)     (N,1) 실수   tf.reduce_mean(tf.square(h-Y))

 이진 분류   sigmoid        (N,1) 0/1    -tf.reduce_mean(
                                            Y*log(h) + (1-Y)*log(1-h))

 다중 분류   softmax        (N,K) one-hot -tf.reduce_mean(
                                            tf.reduce_sum(
                                              Y*log(h+1e-8), axis=1))
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 predicted (예측값 추출)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 선형 회귀   hypothesis 그대로 사용 (연속값)
 이진 분류   tf.cast(hypothesis > 0.5, tf.float32)
 다중 분류   tf.argmax(hypothesis, axis=1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 accuracy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 선형 회귀   tf.sqrt(tf.reduce_mean(tf.square(h - Y)))  → RMSE
 이진 분류   tf.reduce_mean(tf.cast(tf.equal(pred, Y), tf.float32))
 다중 분류   tf.reduce_mean(tf.cast(tf.equal(
                 tf.argmax(h,1), tf.argmax(Y_onehot,1)  ← one-hot Y
                 # 또는 tf.cast(labels, tf.int64)        ← 정수 Y
             ), tf.float32))
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 레이어 선언 패턴 (sigmoid / softmax)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 W shape : [이전층 크기, 다음층 크기]
 b shape : [다음층 크기]

 은닉층 :  layer = tf.sigmoid(tf.matmul(입력, W) + b)
 출력층 :  이진분류 → tf.sigmoid(...)
           다중분류 → tf.nn.softmax(...)
           회귀     → tf.matmul(...) + b  (활성화 없음)

 레이어 연결 시 차원 흐름 예시 (XOR 다층):
  X(N,2) → W1(2,2) → layer1(N,2) → W2(2,1) → hypothesis(N,1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 TensorBoard 선언 패턴
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. 선언부 (sess 밖)
    with tf.name_scope("이름"):         ← 그래프 그룹화 (시각화용)
        W = tf.Variable(...)
        tf.summary.histogram("W", W)   ← 분포 기록 (벡터/행렬)
        tf.summary.scalar("cost", cost) ← 추이 기록 (숫자 1개)

 2. Session 시작 직후
    merged_summary = tf.summary.merge_all()           ← summary 통합
    writer = tf.summary.FileWriter("./logs/폴더명")   ← 저장 위치
    writer.add_graph(sess.graph)                      ← 그래프 저장

 3. 학습 루프 안
    _, summary, cost_val = sess.run(
        [train, merged_summary, cost], feed_dict=...)
    writer.add_summary(summary, global_step=step)     ← step마다 기록

 4. 터미널에서 실행
    tensorboard --logdir=./logs/폴더명
    → 브라우저 http://localhost:6006 접속
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 암기 포인트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. XOR은 비선형 → 단층 불가 → 다층 필요
 2. 다층에서 은닉층이 비선형 변환(sigmoid) → 선형 분리 가능하게 변환
 3. BCE  : - 붙임 / reduce_mean / Y*log(h) + (1-Y)*log(1-h)
    CCE  : - 붙임 / reduce_mean(reduce_sum(axis=1)) / +1e-8
    MSE  : - 없음 / reduce_mean / tf.square(h-Y)
 4. TensorBoard : merge_all → FileWriter → add_graph → add_summary
 5. name_scope  : 시각화 그룹화용, 연산에는 영향 없음
 6. scalar vs histogram : 숫자1개→scalar / 가중치분포→histogram
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# =============================================================================
# [8]  [추가] Queue Runner — 대용량 데이터 파이프라인
# =============================================================================
#
#  왜 필요한가?
#  기존 feed_dict={X: x_data} 방식은 학습할 데이터를 메모리(RAM)에 한 번에 올려야 합니다.
#  하지만 데이터가 수십 GB 단위로 커지면 OOM(Out of Memory) 에러가 발생합니다.
#  -> 이를 해결하기 위해 파일에서 데이터를 펌프질하듯 조금씩 읽어오는 Queue Runner를 사용합니다.
#
#  ── 1. 파일 이름 큐(Queue) 생성 ───────────────────────────────────────────
#  filename_queue = tf.train.string_input_producer(
#      ['data-01.csv', 'data-02.csv'], 
#      shuffle=False, 
#      name='filename_queue'
#  )
#
#  ── 2. 리더(Reader) & 디코더(Decoder) 정의 ─────────────────────────────────
#  reader = tf.TextLineReader()
#  key, value = reader.read(filename_queue)
#
#  # 읽어올 데이터의 기본 타입 지정 (예: 피처 3개는 float, 정답 1개는 int)
#  record_defaults = [[0.], [0.], [0.], [0]] 
#  xy = tf.decode_csv(value, record_defaults=record_defaults)
#
#  ── 3. 배치(Batch) 생성 ───────────────────────────────────────────────────
#  # 데이터를 모아서 한 번에 학습할 단위(batch)로 묶어줍니다.
#  train_x_batch, train_y_batch = tf.train.batch(
#      [xy[0:-1], xy[-1:]],   # [X데이터(슬라이싱), Y데이터(슬라이싱)]
#      batch_size=10          # 한 번에 10개씩 뽑음
#  )
#
#  ── 4. Session 내 실행 (Coordinator 필수) ─────────────────────────────────
#  # Queue Runner는 멀티 스레드로 동작하므로 스레드 관리자(Coordinator)가 필요합니다.
#  with tf.Session() as sess:
#      # 스레드 코디네이터 생성 및 큐 러너 시작 (펌프 가동)
#      coord = tf.train.Coordinator()
#      threads = tf.train.start_queue_runners(sess=sess, coord=coord)
#
#      for step in range(2000):
#          # feed_dict 대신, batch 노드를 run()하여 데이터를 뽑아옵니다.
#          x_batch, y_batch = sess.run([train_x_batch, train_y_batch])
#          
#          # 뽑아온 배치 데이터를 이용해 학습 진행
#          # cost_val, _ = sess.run([cost, train], feed_dict={X: x_batch, Y: y_batch})
#
#      # 학습 종료 후 스레드 안전하게 정지
#      coord.request_stop()
#      coord.join(threads)
# =============================================================================