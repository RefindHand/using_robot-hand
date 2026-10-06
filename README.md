# using_robot-hand

ROS2 Humble과 MuJoCo를 이용해 로봇 핸드 제어를 연습하기 위한 프로젝트입니다.

실물 로봇 핸드를 사용하기 전에 ROS2의 Topic, Publisher/Subscriber 구조를 이용해
가상의 ROHand 모델을 직접 움직여 보는 것을 목표로 합니다.

## 현재 진행 상황

현재 다음 기능까지 구현 및 확인했습니다.

- WSL2 + Ubuntu 22.04 환경
- ROS2 Humble
- MuJoCo 실행
- OYMotion 공식 ROHand MuJoCo 모델 사용
- ROS2 `sensor_msgs/JointState` 메시지를 이용한 제어
- `/target_joint_state` Topic을 통해 MuJoCo 로봇 핸드 제어
- 오른손 모델의 검지(Index Finger) 제어 확인 완료

현재 제어 흐름은 다음과 같습니다.

```text
ROS2 Publisher
      |
      v
/target_joint_state
      |
      v
mujoco_bridge
      |
      v
MuJoCo ROHand Model
```

GUI 제어 기능은 이후 추가할 예정입니다.

---

# 1. 환경

현재 테스트한 환경:

```text
Windows + WSL2
Ubuntu 22.04
ROS2 Humble
Python 3.10
MuJoCo
```

ROS2 Humble이 이미 설치되어 있다고 가정합니다.

확인:

```bash
source /opt/ros/humble/setup.bash
ros2 --help
```

---

# 2. Repository Clone

```bash
cd ~
git clone https://github.com/RefindHand/using_robot-hand.git
cd using_robot-hand
```

---

# 3. MuJoCo 설치

```bash
python3 -m pip install --user mujoco
```

확인:

```bash
python3 -c "import mujoco; print(mujoco.__version__)"
```

---

# 4. ROHand MuJoCo 모델 다운로드

본 프로젝트에서는 OYMotion에서 제공하는 공식 MuJoCo 모델을 사용합니다.

```bash
mkdir -p external

git clone https://github.com/oymotion/rohand_mujoco.git \
external/rohand_mujoco
```

`external/` 폴더는 Git에 포함하지 않습니다.

---

# 5. ROS2 Package Build

Repository 루트에서 실행합니다.

```bash
source /opt/ros/humble/setup.bash

colcon build --symlink-install

source install/setup.bash
```

정상적으로 빌드되었는지 확인:

```bash
ros2 pkg list | grep refine_hand_control
```

다음과 같이 나오면 됩니다.

```text
refine_hand_control
```

---

# 6. MuJoCo ROS2 Bridge 실행

첫 번째 터미널에서:

```bash
cd ~/using_robot-hand

source /opt/ros/humble/setup.bash
source install/setup.bash

LIBGL_ALWAYS_SOFTWARE=1 \
ros2 run refine_hand_control mujoco_bridge
```

정상적으로 실행되면 MuJoCo 창에 오른손 모델이 나타나고 다음과 비슷한 메시지가 출력됩니다.

```text
Listening on /target_joint_state
```

---

# 7. 손가락 움직여 보기

새 터미널을 하나 더 엽니다.

```bash
cd ~/using_robot-hand

source /opt/ros/humble/setup.bash
source install/setup.bash
```

검지를 구부립니다.

```bash
ros2 topic pub --once \
/target_joint_state \
sensor_msgs/msg/JointState \
"{name: ['index_finger'], position: [1.0]}"
```

MuJoCo에서 검지가 움직이면 성공입니다.

검지를 다시 펴려면:

```bash
ros2 topic pub --once \
/target_joint_state \
sensor_msgs/msg/JointState \
"{name: ['index_finger'], position: [0.0]}"
```

# 8. GUI 실행

첫 번째 터미널:

```bash
cd ~/Desktop/using_robot-hand
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 run refine_hand_control mujoco_bridge
```
```bash
cd ~/Desktop/using_robot-hand
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run refine_hand_control hand_gui
```


---

## 현재 구현 상태

- [x] MuJoCo 설치 및 실행
- [x] ROHand 모델 표시
- [x] ROS2 package 생성
- [x] ROS2 → MuJoCo bridge
- [x] ROS2 Topic을 이용한 손가락 제어
- [x] GUI Slider 제어
- [ ] 실행 과정 간소화
- [ ] 팀원용 최종 Setup Guide
---

<details>
<summary>WSL에서 MuJoCo 화면이 검게 나오는 경우</summary>

WSL 환경에서 MuJoCo 창은 열리지만 모델이 보이지 않는 경우가 있습니다.

이 프로젝트에서는 다음과 같이 software rendering을 사용하여 실행했습니다.

```bash
LIBGL_ALWAYS_SOFTWARE=1 \
ros2 run refine_hand_control mujoco_bridge
```

</details>

<details>
<summary>프로젝트 구조</summary>

현재 주요 구조는 다음과 같습니다.

```text
using_robot-hand/
├── README.md
├── src/
│   └── refine_hand_control/
│       ├── package.xml
│       ├── setup.py
│       ├── setup.cfg
│       │
│       └── refine_hand_control/
│           ├── __init__.py
│           └── mujoco_bridge.py
│
└── external/
    └── rohand_mujoco/
```

`external/`, `build/`, `install/`, `log/` 폴더는 Git에서 제외합니다.

</details>

---

## Next Step

다음 단계에서는 별도의 ROS2 GUI Node를 추가하여

```text
GUI Slider
    |
    v
/target_joint_state
    |
    v
MuJoCo Bridge
    |
    v
Virtual ROHand
```

구조로 각 손가락을 슬라이더를 이용해 제어할 예정입니다.