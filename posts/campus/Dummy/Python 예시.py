# =============================================================================
#  Cost 함수 완전 정복
#  선형회귀 / 이진분류(sigmoid) / 다중분류(softmax+one-hot)
#  — 왜 이렇게 쓰는지, 수식과 코드 전부
# =============================================================================
#
#  ┌─────────────────────────────────────────────────────────────────┐
#  │  문제 유형          출력층        Cost 함수                      │
#  │  ───────────────────────────────────────────────────────────── │
#  │  선형 회귀          없음(선형)    MSE  (평균 제곱 오차)          │
#  │  이진 분류          sigmoid       BCE  (이진 크로스엔트로피)     │
#  │  다중 분류(one-hot) softmax       CCE  (범주형 크로스엔트로피)   │
#  └─────────────────────────────────────────────────────────────────┘

import tensorflow as tf
import numpy as np
tf.set_random_seed(777)


# =============================================================================
# ① MSE  (Mean Squared Error)  — 선형 회귀
# =============================================================================
#
#  ● 언제?
#    출력이 "연속적인 숫자" 일 때
#    예) 집값 예측, 기온 예측, 시험 점수 예측
#
#  ● 왜 MSE?
#    예측값과 정답의 "거리(오차)"를 제곱해서 평균냄
#    제곱하는 이유 : 오차가 양수든 음수든 항상 양수로 만들기 위해
#                  + 큰 오차에 더 큰 패널티를 줌
#
#  수식 :  MSE = (1/N) * Σ (hypothesis - Y)²
#
#  ● 출력층 : 활성화함수 없음 (그냥 선형)
#    hypothesis = X @ W + b    ← 어떤 실수값이든 출력 가능

X_reg = tf.placeholder(tf.float32, [None, 3])   # 입력 피처 3개
Y_reg = tf.placeholder(tf.float32, [None, 1])   # 정답 (연속값)

W_reg = tf.Variable(tf.random_normal([3, 1]))
b_reg = tf.Variable(tf.random_normal([1]))

hypothesis_reg = tf.matmul(X_reg, W_reg) + b_reg   # 활성화함수 없음!
#  출력 범위 : -∞ ~ +∞   (실수 전체)

# ── MSE Cost ─────────────────────────────────────────────────────────────
cost_mse = tf.reduce_mean(tf.square(hypothesis_reg - Y_reg))
#  tf.square(hypothesis - Y)   : (예측 - 정답)²  — 원소별 제곱
#  tf.reduce_mean(...)         : 전체 샘플 평균   — 스칼라 하나

# 동일한 표현들 (전부 같은 결과)
# cost_mse = tf.reduce_mean((hypothesis_reg - Y_reg) ** 2)
# cost_mse = tf.reduce_mean(tf.pow(hypothesis_reg - Y_reg, 2))

train_reg = tf.train.GradientDescentOptimizer(0.01).minimize(cost_mse)

# [실행 예시]
"""
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for step in range(2001):
        _, c = sess.run([train_reg, cost_mse],
                        feed_dict={X_reg: x_data, Y_reg: y_data})
        if step % 200 == 0:
            print("Step:", step, "  Cost:", c)
    # Cost가 낮아질수록 예측이 정답에 가까워짐
"""


# =============================================================================
# ② BCE  (Binary Cross-Entropy)  — 이진 분류 (sigmoid)
# =============================================================================
#
#  ● 언제?
#    출력이 "둘 중 하나" 일 때  (0 or 1)
#    예) 생존/사망, 스팸/정상, 합격/불합격, 질병 유무
#
#  ● 왜 BCE?  (MSE를 쓰면 안 되는 이유)
#    sigmoid 출력은 0~1 사이 곡선
#    → MSE + sigmoid 조합은 기울기(gradient)가 매우 작아져서 학습이 느려짐
#       (Vanishing Gradient 문제)
#    → log를 쓰면 기울기가 살아나서 학습이 빠르고 안정적
#
#  수식 :  BCE = -(1/N) * Σ [ Y*log(h)  +  (1-Y)*log(1-h) ]
#
#    Y=1 일 때 : -(1*log(h) + 0)  =  -log(h)
#               → h(예측)가 1에 가까울수록 cost ↓  (올바른 방향)
#    Y=0 일 때 : -(0 + 1*log(1-h)) = -log(1-h)
#               → h(예측)가 0에 가까울수록 cost ↓
#
#  ● 출력층 : sigmoid
#    hypothesis = sigmoid(X @ W + b)   → 출력 범위 0~1

X_bin = tf.placeholder(tf.float32, [None, 17])
Y_bin = tf.placeholder(tf.float32, [None,  1])   # 정답 : 0.0 또는 1.0

W_bin = tf.Variable(tf.random_normal([17, 1]))
b_bin = tf.Variable(tf.random_normal([1]))

hypothesis_bin = tf.sigmoid(tf.matmul(X_bin, W_bin) + b_bin)
#  출력 범위 : 0 ~ 1  (확률처럼 해석)

# ── BCE Cost ─────────────────────────────────────────────────────────────
cost_bce = -tf.reduce_mean(
    Y_bin * tf.log(hypothesis_bin) +
    (1 - Y_bin) * tf.log(1 - hypothesis_bin)
)
#  [왜 마이너스(-)를 붙이나?]
#  log는 항상 음수값 → 마이너스를 붙여야 "최소화"했을 때 정답에 수렴
#  minimize(cost) 이므로 cost가 작아지는 방향 = 정답에 가까워지는 방향
#
#  [왜 +1e-8을 안 붙였나?]
#  이론상 hypothesis=0 or 1 이 되면 log(0)=-inf
#  → 실제로는 잘 안 일어나지만 안정성 위해 붙이는 게 더 좋음
#  cost_bce_safe = -tf.reduce_mean(
#      Y_bin * tf.log(hypothesis_bin + 1e-8) +
#      (1 - Y_bin) * tf.log(1 - hypothesis_bin + 1e-8))

# ── BCE 내장 함수 버전 (더 수치 안정적) ──────────────────────────────────
# logits_bin = tf.matmul(X_bin, W_bin) + b_bin  # sigmoid 적용 전 값
# cost_bce_builtin = tf.reduce_mean(
#     tf.nn.sigmoid_cross_entropy_with_logits(
#         logits=logits_bin,   # ← sigmoid 전 값을 넣음!
#         labels=Y_bin
#     )
# )
# [주의] 내장 함수는 sigmoid를 내부에서 처리하므로 logits(sigmoid 전)를 넣어야 함

# ── Predicted & Accuracy ─────────────────────────────────────────────────
predicted_bin = tf.cast(hypothesis_bin > 0.5, dtype=tf.float32)
#  0.5 기준 : 확률 > 0.5 이면 1 (양성), 그 이하면 0 (음성)

accuracy_bin = tf.reduce_mean(
    tf.cast(tf.equal(predicted_bin, Y_bin), dtype=tf.float32)
)

train_bin = tf.train.GradientDescentOptimizer(0.2).minimize(cost_bce)

# [실행 예시]
"""
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for step in range(20001):
        _, c = sess.run([train_bin, cost_bce],
                        feed_dict={X_bin: x_data, Y_bin: y_data})
        if step % 1000 == 0:
            print("Step:", step, "  Cost:", c)

    h, pred, acc = sess.run([hypothesis_bin, predicted_bin, accuracy_bin],
                             feed_dict={X_bin: x_data, Y_bin: y_data})
    print("Accuracy:", acc)
    # pred : [[1.][0.][1.] ...]  (예측값)
    # acc  : 0.85 같은 0~1 사이 숫자
"""


# =============================================================================
# ③ CCE  (Categorical Cross-Entropy)  — 다중 분류 (softmax + one-hot)
# =============================================================================
#
#  ● 언제?
#    출력이 "여러 클래스 중 하나" 일 때
#    예) 숫자 0~9 분류(MNIST), 고양이/개/새 분류, 감정 분류
#
#  ● 왜 CCE?
#    softmax 출력은 각 클래스의 확률 벡터 (합=1)
#    정답(one-hot)에서 1인 자리의 log 확률만 뽑아서 최대화하는 구조
#    BCE를 클래스 수만큼 확장한 버전
#
#  수식 :  CCE = -(1/N) * Σ Σ Y_onehot * log(hypothesis)
#              (샘플 합) (클래스 합)
#
#    one-hot이므로 정답 클래스만 1, 나머지는 0
#    → 결국 -(정답 클래스의 log 확률) 만 남음
#
#  ● 출력층 : softmax
#    hypothesis = softmax(X @ W + b)  → 클래스별 확률, 합=1

X_mc = tf.placeholder(tf.float32, [None, 4])    # 피처 4개
Y_mc = tf.placeholder(tf.float32, [None, 3])    # one-hot label (클래스 3개)
#  [중요] Y는 one-hot 형태  ex) 클래스1 → [0,1,0]

W_mc = tf.Variable(tf.random_normal([4, 3]))
b_mc = tf.Variable(tf.random_normal([3]))

hypothesis_mc = tf.nn.softmax(tf.matmul(X_mc, W_mc) + b_mc)
#  출력 shape : (N, 3)   각 행의 합 = 1.0

# ── CCE Cost ─────────────────────────────────────────────────────────────
cost_cce = -tf.reduce_mean(
    tf.reduce_sum(Y_mc * tf.log(hypothesis_mc + 1e-8), axis=1)
)
#  Y_mc * tf.log(hypothesis_mc + 1e-8)
#    : (N, 3) 원소별 곱  — one-hot이므로 정답 클래스 자리만 살아남
#    예) Y=[0,1,0], log(hyp)=[-2, -0.1, -3]  →  곱하면 [0, -0.1, 0]
#
#  tf.reduce_sum(..., axis=1)
#    : 각 샘플별로 클래스 방향(axis=1) 합산  → shape (N,)
#    예) [0, -0.1, 0]  →  -0.1
#    [중요] axis=1 을 빠트리면 전체 합이 되어 스칼라가 됨 (잘못된 계산)
#
#  tf.reduce_mean(...)
#    : N개 샘플의 평균  →  스칼라 최종 cost
#
#  [마이너스(-) 이유]
#    log 값은 항상 음수 (0~1 사이 입력이므로)
#    → 마이너스를 붙여 양수로 만들어야 minimize가 의미 있음

# ── CCE 내장 함수 버전 (더 수치 안정적) ──────────────────────────────────
# logits_mc = tf.matmul(X_mc, W_mc) + b_mc   # softmax 적용 전
# cost_cce_builtin = tf.reduce_mean(
#     tf.nn.softmax_cross_entropy_with_logits_v2(
#         logits=logits_mc,   # ← softmax 전 값을 넣음!
#         labels=Y_mc
#     )
# )
# [주의] 내장 함수는 softmax를 내부에서 처리 → logits(softmax 전)를 넣어야 함
# v2를 쓰는 이유 : v1은 deprecated 경고 뜸

# ── Predicted & Accuracy ─────────────────────────────────────────────────
predicted_mc = tf.argmax(hypothesis_mc, axis=1)
#  각 샘플에서 확률이 가장 높은 클래스 인덱스
#  (N, 3) → (N,)   dtype=int64

actual_mc = tf.argmax(Y_mc, axis=1)
#  one-hot label에서 1이 있는 위치 = 실제 클래스 인덱스

accuracy_mc = tf.reduce_mean(
    tf.cast(tf.equal(predicted_mc, actual_mc), dtype=tf.float32)
)

train_mc = tf.train.GradientDescentOptimizer(0.1).minimize(cost_cce)

# [실행 예시]
"""
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for step in range(2001):
        _, c = sess.run([train_mc, cost_cce],
                        feed_dict={X_mc: x_data, Y_mc: y_onehot})
        if step % 200 == 0:
            print("Step:", step, "  Cost:", c)

    pred = sess.run(predicted_mc, feed_dict={X_mc: x_data})
    print("Predictions:", pred)   # [0, 2, 1, 1, 2 ...]
"""


# =============================================================================
# ④ MNIST 버전 — iterator + CCE  (실제 시험 코드에 가장 가까운 버전)
# =============================================================================
#
#  MNIST에서의 차이점
#  - Y가 정수 레이블 (0~9) 로 들어옴  → one_hot 변환 필요
#  - iterator에서 labels를 int32로 받아서 one_hot 적용
#  - predicted와 비교 시 labels를 int64로 캐스팅

# (iterator에서 받은 텐서 가정)
# features : (100, 784)  tf.float32
# labels   : (100,)      tf.int32

# labels_onehot = tf.one_hot(labels, depth=10)   # (100,) → (100, 10)
# hypothesis    : (100, 10)  softmax 출력

# ── MNIST CCE Cost ────────────────────────────────────────────────────────
# cost = -tf.reduce_mean(labels_onehot * tf.log(hypothesis + 1e-8))
#
# [reduce_sum 없이 reduce_mean만 쓰는 이유]
# labels_onehot * tf.log(hypothesis + 1e-8) : (100, 10)
# one-hot이므로 각 행에서 정답 클래스 1개만 살아남고 나머지는 0
# → 각 행의 유효한 값이 1개뿐이므로 reduce_sum(axis=1) 을 해도 결과가 같음
# → reduce_mean이 (100, 10) 전체 900개를 평균내도 0인 자리는 기여 없음
# → 결과적으로 같은 방향의 gradient를 만듦 (스케일 차이는 있음)
#
# ★ 더 엄밀하게 쓰려면:
# cost = -tf.reduce_mean(tf.reduce_sum(labels_onehot * tf.log(hypothesis + 1e-8), axis=1))
# 이 쪽이 표준 CCE와 완전히 동일

# predicted = tf.argmax(hypothesis, axis=1)            # int64
# accuracy  = tf.reduce_mean(
#     tf.cast(tf.equal(predicted, tf.cast(labels, tf.int64)), tf.float32))
# [중요] labels(int32) vs predicted(int64) 타입 불일치 → int64로 캐스팅 필수


# =============================================================================
# 전체 비교표
# =============================================================================
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 문제        출력층       Y shape    Cost 코드
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 선형회귀    없음(선형)   (N,1)      tf.reduce_mean(tf.square(hyp - Y))

 이진분류    sigmoid      (N,1)      -tf.reduce_mean(
                         0.0/1.0        Y * tf.log(hyp) +
                                       (1-Y) * tf.log(1-hyp))

 다중분류    softmax      (N,K)      -tf.reduce_mean(
            (K=클래스수) one-hot        tf.reduce_sum(
                                           Y * tf.log(hyp + 1e-8), axis=1))
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 predicted
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 선형회귀    → 그대로 사용 (연속값)      hyp 자체가 예측값
 이진분류    → tf.cast(hyp > 0.5, tf.float32)
 다중분류    → tf.argmax(hyp, axis=1)   (가장 높은 확률의 클래스 인덱스)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 accuracy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 선형회귀    → 보통 RMSE 사용  tf.sqrt(tf.reduce_mean(tf.square(hyp - Y)))
 이진분류    → tf.reduce_mean(tf.cast(tf.equal(pred, Y), tf.float32))
 다중분류    → tf.reduce_mean(
                  tf.cast(tf.equal(
                      tf.argmax(hyp, 1),
                      tf.argmax(Y_onehot, 1)     ← one-hot 레이블
                      # 또는 tf.cast(labels, tf.int64)  ← 정수 레이블
                  ), tf.float32))
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 핵심 암기 포인트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1. MSE      = tf.reduce_mean(tf.square(hyp - Y))
              → 회귀에서만 사용, 활성화함수 없음

 2. BCE      = -tf.reduce_mean(Y*log(h) + (1-Y)*log(1-h))
              → 이진분류, sigmoid, Y는 0/1

 3. CCE      = -tf.reduce_mean(tf.reduce_sum(Y*log(h+1e-8), axis=1))
              → 다중분류, softmax, Y는 one-hot
              → axis=1 이 핵심 (클래스 방향 합산)
              → +1e-8 필수 (log 0 방지)

 4. 마이너스(-) : log 값이 음수이므로 cost를 양수로 만들기 위해 필수
 5. reduce_mean : 배치 전체 평균내서 스칼라 하나로
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
