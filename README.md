# 🏀 Basketball Shoot Game

Python의 tkinter로 만든 간단한 농구 슛 게임입니다.
방향키로 각도를 조절하고, 스페이스바를 눌렀다 놓아 슛합니다.

## 실행 환경
- Python 3
- tkinter
- 그래픽 화면을 사용할 수 있는 PC

별도 pip 패키지는 필요하지 않습니다.
일부 Linux 환경에서는 tkinter를 별도로 설치해야 합니다.

## 실행 방법
1. 이 저장소에서 Code → Download ZIP을 선택합니다.
2. 압축을 풉니다.
3. 압축을 푼 폴더에서 아래 명령을 실행합니다.

```bash
python basketball_game.py
```

Windows에서 python 명령이 인식되지 않으면:

```bash
py basketball_game.py
```

## 조작법
| 키 | 기능 |
|---|---|
| ← / ↑ | 슛 각도 높이기 |
| → / ↓ | 슛 각도 낮추기 |
| 스페이스바 누르기 | 힘 모으기 |
| 스페이스바 놓기 | 슛 |
| R | 점수 초기화 |
| ESC | 종료 |

## 게임 규칙
- 슛 성공 시 2점
- 성공률과 연속 성공 횟수 표시
- 슛이 끝나면 다음 공 자동 준비

## 참고
PC에서 실행하는 게임입니다.
GitHub 페이지 안에서 바로 플레이할 수는 없습니다.
