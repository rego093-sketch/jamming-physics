폰트 서브셋(woff2 2~3)은 저자 로컬 단계: 본문 세리프/시스템 스택이 기본이며, 커스텀 폰트 채택 시
`pyftsubset Font.ttf --flavor=woff2 --unicodes=U+0000-00FF,U+2070-209F,U+2200-22FF,U+0370-03FF` 로 생성 후
site.css 상단에 @font-face 추가 + preload 1개만. (네트워크 차단 환경이라 Phase 0 세션은 스택 기본값 채택 — 결정 기록)
