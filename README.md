# using_robot-hand

ROS2 Humble과 MuJoCo를 이용해 **가상 ROHand를 직접 제어해 보는 연습용 프로젝트**입니다.

실물 로봇 핸드를 사용하기 전에 ROS2의 Topic과 Publisher/Subscriber 구조를 이용해
손가락 제어를 경험하는 것이 목적입니다.

현재는 **MuJoCo 오른손 모델 + ROS2 Bridge + 슬라이더 GUI 제어**까지 동작을 확인했습니다.

---

# 빠른 시작

## 0. 준비 환경

다음 환경이 준비되어 있다고 가정합니다.

```text
Windows + WSL2
Ubuntu 22.04
ROS2 Humble
Python 3.10
```

ROS2가 정상적으로 설치되어 있는지 확인합니다.

```bash
source /opt/ros/humble/setup.bash
ros2 --help
```

---

## 1. Repository 받기

### 처음 받는 경우

```bash
cd ~
git clone https://github.com/RefindHand/using_robot-hand.git
cd using_robot-hand
```

### 이미 Clone한 경우

```bash
cd ~/using_robot-hand
git pull origin main
```

---

## 2. 필요한 패키지 설치

```bash
sudo apt install -y python3-tk python3-colcon-common-extensions
python3 -m pip install --user mujoco
```

MuJoCo 설치 확인:

```bash
python3 -c "import mujoco; print('MuJoCo:', mujoco.__version__)"
```

---

## 3. ROHand MuJoCo 모델 받기

이 프로젝트는 OYMotion에서 제공하는 공식 MuJoCo 모델을 사용합니다.

```bash
cd ~/using_robot-hand

mkdir -p external
git clone https://github.com/oymotion/rohand_mujoco.git external/rohand_mujoco
```

`external/` 폴더는 Git에 포함하지 않습니다.

---

## 4. ROS2 패키지 빌드

Repository 루트에서 실행합니다.

```bash
cd ~/using_robot-hand

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

# 실행

## 5. MuJoCo 실행

첫 번째 터미널에서 실행합니다.

```bash
cd ~/using_robot-hand

source /opt/ros/humble/setup.bash
source install/setup.bash

LIBGL_ALWAYS_SOFTWARE=1 ros2 run refine_hand_control mujoco_bridge
```

정상적으로 실행되면 MuJoCo 창에 오른손 모델이 나타나고 터미널에 다음과 비슷한 메시지가 표시됩니다.

```text
Listening on /target_joint_state
```

MuJoCo 창은 그대로 켜 둡니다.

---

## 6. GUI로 손가락 움직이기

새 WSL 터미널을 하나 더 열고 실행합니다.

```bash
cd ~/using_robot-hand

source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run refine_hand_control hand_gui
```

GUI에 다음 6개의 슬라이더가 나타납니다.

```text
Index
Middle
Ring
Little
Thumb Rotate
Thumb Bend
```

슬라이더를 움직이면 ROS2의 `/target_joint_state` Topic을 통해
MuJoCo의 ROHand 모델이 움직입니다.

`Open All / Reset` 버튼을 누르면 모든 슬라이더가 0으로 돌아갑니다.

---

# 터미널에서 직접 제어해 보기

GUI 대신 ROS2 Topic을 직접 Publish해서 손가락을 움직일 수도 있습니다.

MuJoCo Bridge를 실행한 상태에서 새 터미널을 열고:

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

검지를 다시 폅니다.

```bash
ros2 topic pub --once \
/target_joint_state \
sensor_msgs/msg/JointState \
"{name: ['index_finger'], position: [0.0]}"
```

직접 Topic을 Publish할 때 `position` 값은 **radian**입니다.

<<<<<<< HEAD
첫 번째 터미널:
```bash
cd ~/Desktop/using_robot-hand
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 run refine_hand_control mujoco_bridge
```

 두 번째 터미널:
```bash
cd ~/Desktop/using_robot-hand
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run refine_hand_control hand_gui
```

=======
---

# 현재 제어 구조

```text
GUI / ROS2 Topic Command
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

현재 사용하는 MuJoCo actuator 이름은 다음과 같습니다.

```text
index_finger
middle_finger
ring_finger
little_finger
thumb_root
thumb
```

GUI에서는 사용하기 편하도록 각도를 degree 단위로 표시하고,
내부에서 radian으로 변환하여 ROS2 메시지를 전송합니다.
>>>>>>> 349c3fa (Refine setup and GUI guide)

---

# 현재 구현 상태

- [x] MuJoCo 설치 및 실행
- [x] ROHand 오른손 모델 표시
- [x] ROS2 Python Package 구성
- [x] ROS2 → MuJoCo Bridge
- [x] `/target_joint_state` Topic을 이용한 손가락 제어
- [x] 6개 관절 GUI Slider 제어
- [x] Open All / Reset
- [ ] 실행 과정 간소화
- [ ] 실물 ROHand 연동
- [ ] Tactile Sensor 연동

---

<details>
<summary><strong>WSL에서 MuJoCo 창이 검게 나오는 경우</strong></summary>

WSL 환경에서는 MuJoCo 창은 열리지만 화면이 검게 보일 수 있습니다.

이 프로젝트에서는 Software Rendering을 사용하면 정상적으로 표시되었습니다.

```bash
LIBGL_ALWAYS_SOFTWARE=1 ros2 run refine_hand_control mujoco_bridge
```

</details>

<details>
<summary><strong>프로젝트 구조 보기</strong></summary>

```text
using_robot-hand/
├── README.md
├── .gitignore
│
├── src/
│   └── refine_hand_control/
│       ├── package.xml
│       ├── setup.py
│       ├── setup.cfg
│       │
│       └── refine_hand_control/
│           ├── __init__.py
│           ├── mujoco_bridge.py
│           └── hand_gui.py
│
└── external/
    └── rohand_mujoco/
```

다음 폴더들은 Git에서 제외합니다.

```text
external/
build/
install/
log/
.vscode/
```

</details>

---

# 참고

- ROHand MuJoCo Model  
  https://github.com/oymotion/rohand_mujoco

- ROS2 Humble Documentation  
  https://docs.ros.org/en/humble/