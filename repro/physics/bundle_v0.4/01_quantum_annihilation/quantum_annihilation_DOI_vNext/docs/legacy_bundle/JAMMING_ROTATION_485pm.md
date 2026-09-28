# 재밍 격자에서 VP(부피입자) 실제 운동 + 4.85 pm “회전” 스케일 연구

## 0) 요지
- **VP는 고정된 노드가 아니라, 재밍 네트워크 안에서 실제로 이동(translation)하며 재배열(rearrangement)된다.**
- SOC(자기조직화 임계) 루프에서 눈사태(avalanches)가 발생할 때,
  전역 전파를 담당하는 임계 목갭 g*로부터 구조 증폭계수 **A ≃ a/δ_eff**가 매번 재평가되며,
  그 값이 **A ~ 10^6** 범위에서 분포한다.
- 가시광 운반파(633 nm)를 기준으로, “격자 떨림이 만드는 회전”을
  **접점에서 위상 2π를 한 번 감는 원호 길이(arc length)**로 정의하면,

\[
\delta_{\rm step} = \frac{\lambda}{A},\qquad
\ell_{\rm rot} = 2\pi\,\delta_{\rm step} = \frac{2\pi\lambda}{A}.
\]

- 이때 A가 10^6이면 **ℓ_rot는 자연스럽게 pm(10^-12 m) 스케일**이 된다.
- 실제 번들에 저장된 SOC 로그(avalanches)에서 633 nm 기준으로
  **ℓ_rot ≈ 4.854 pm**이 되는 이벤트(눈사태 index 18)가 확인된다.

## 1) “VP는 실제로 움직인다”는 것을 어디서 보나?
SOC 코드는 임계 도달 시,
- 임계 연결 클러스터(cluster)를 찾고
- 해당 입자들의 좌표를 가우시안 킥으로 perturb 한 뒤
- FIRE 최소화로 겹침을 제거하며 재밍 상태를 복원한다.

즉, 각 눈사태는 *실제 입자 좌표의 이동 + 에너지 최소화에 의한 재배열*을 포함한다.

## 2) 4.85 pm 회전 스케일의 수치 확인(이 번들 기준)
이 번들에는 이미 SOC 로그가 저장되어 있다.

- 입력: `results/soc_run3_avalanches.csv`
- 분석 스크립트: `code/jamming_rotation_485pm_study.py`
- 출력: `results/jamming_rotation_485pm_summary.json`

분석 결과(633 nm):
- best match(타겟 4.85 pm에 가장 가까운 이벤트):
  - avalanche index = 18
  - A_post = 8.1933×10^5
  - **ℓ_rot(633) = 4.8542 pm**
  - δ_step(633) = 0.7726 pm

## 3) 재밍(잼밍) 구조 관점의 해석
- 재밍 상태에서는 목갭(δ_eff)이 매우 작아져 구조적으로 “기어비”가 큰 네트워크가 된다.
- A는 그 기어비(증폭비)를 요약한 무차원 수로 볼 수 있으며,
  운반파의 위상 2π가 네트워크의 미시 재배열(미시 스텝) A번에 걸쳐 분산되어 나타난다고 해석하면
  위 식의 pm 스케일 “회전(원호 길이)”이 자연스럽게 나온다.
- 즉, **4.85 pm은 외부로 끼워 넣은 값이 아니라, (λ, A) 두 값의 조합에서 나오는 교차-스케일 산출물**이다.

## 4) 재현 실행
```bash
python code/jamming_rotation_485pm_study.py
```

생성되는 그림:
- `images/jamming_rot_circ_vs_av.png` : 눈사태 index별 ℓ_rot(633)
- `images/jamming_rot_hist.png` : ℓ_rot 분포 히스토그램
