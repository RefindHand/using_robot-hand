from pathlib import Path

import mujoco
import mujoco.viewer
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


ACTUATORS = [
    'index_finger',
    'middle_finger',
    'ring_finger',
    'little_finger',
    'thumb_root',
    'thumb',
]


class MuJoCoBridge(Node):

    def __init__(self):
        super().__init__('mujoco_bridge')

        model_path = (
            Path.cwd()
            / 'external/rohand_mujoco'
            / 'A001&A002/model/rohand_right.xml'
        )

        self.model = mujoco.MjModel.from_xml_path(str(model_path))
        self.data = mujoco.MjData(self.model)

        self.ids = {
            name: mujoco.mj_name2id(
                self.model,
                mujoco.mjtObj.mjOBJ_ACTUATOR,
                name
            )
            for name in ACTUATORS
        }

        self.create_subscription(
            JointState,
            'target_joint_state',
            self.command_callback,
            10
        )

        self.viewer = mujoco.viewer.launch_passive(
            self.model,
            self.data
        )

        self.create_timer(0.01, self.update)

        self.get_logger().info(
            'Listening on /target_joint_state'
        )

    def command_callback(self, msg):
        for name, position in zip(msg.name, msg.position):

            if name not in self.ids:
                continue

            actuator_id = self.ids[name]
            low, high = self.model.actuator_ctrlrange[actuator_id]

            position = max(low, min(high, float(position)))
            self.data.ctrl[actuator_id] = position

            self.get_logger().info(
                f'{name} -> {position:.2f} rad'
            )

    def update(self):
        if not self.viewer.is_running():
            rclpy.shutdown()
            return

        for _ in range(5):
            mujoco.mj_step(self.model, self.data)

        self.viewer.sync()


def main(args=None):
    rclpy.init(args=args)

    node = MuJoCoBridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()

    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()