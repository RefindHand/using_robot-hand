import math
import tkinter as tk

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


JOINTS = {
    'Index': ('index_finger', 82.5),
    'Middle': ('middle_finger', 82.5),
    'Ring': ('ring_finger', 82.5),
    'Little': ('little_finger', 82.5),
    'Thumb Rotate': ('thumb_root', 90.0),
    'Thumb Bend': ('thumb', 57.0),
}


class HandGui(Node):
    def __init__(self):
        super().__init__('hand_gui')

        self.publisher = self.create_publisher(
            JointState,
            '/target_joint_state',
            10
        )

        self.root = tk.Tk()
        self.root.title('Refind Hand Control')

        self.sliders = {}

        for label, (joint_name, max_degree) in JOINTS.items():
            frame = tk.Frame(self.root)
            frame.pack(fill='x', padx=20, pady=5)

            tk.Label(
                frame,
                text=label,
                width=14,
                anchor='w'
            ).pack(side='left')

            slider = tk.Scale(
                frame,
                from_=0,
                to=max_degree,
                orient='horizontal',
                resolution=1,
                length=300,
                command=lambda value, name=joint_name:
                    self.publish_joint(name, float(value))
            )

            slider.pack(side='left')
            self.sliders[joint_name] = slider

        tk.Button(
            self.root,
            text='Open All / Reset',
            command=self.reset_all
        ).pack(pady=15)

        self.root.protocol('WM_DELETE_WINDOW', self.close)

    def publish_joint(self, joint_name, degree):
        msg = JointState()
        msg.name = [joint_name]
        msg.position = [math.radians(degree)]

        self.publisher.publish(msg)

    def reset_all(self):
        for slider in self.sliders.values():
            slider.set(0)

    def run(self):
        self.root.mainloop()

    def close(self):
        self.root.destroy()


def main(args=None):
    rclpy.init(args=args)

    node = HandGui()

    try:
        node.run()
    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()