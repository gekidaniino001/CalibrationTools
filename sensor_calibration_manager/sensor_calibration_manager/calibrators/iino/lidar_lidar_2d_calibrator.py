#!/usr/bin/env python3

# Copyright 2025 TIER IV, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict

import numpy as np

from sensor_calibration_manager.calibrator_base import CalibratorBase
from sensor_calibration_manager.calibrator_registry import CalibratorRegistry
from sensor_calibration_manager.ros_interface import RosInterface
from sensor_calibration_manager.types import FramePair


@CalibratorRegistry.register_calibrator(
    project_name="iino", calibrator_name="lidar_lidar_2d_calibrator"
)
class LidarLidar2DCalibrator(CalibratorBase):
    required_frames = []

    def __init__(self, ros_interface: RosInterface, **kwargs):
        super().__init__(ros_interface)

        self.base_frame = "base_link"
        self.sensor_kit_frame = "sensor_kit_base_link"
        self.source_frame = "velodyne_rear"
        self.source_base_frame = "velodyne_rear_base_link"
        self.target_frame = "velodyne_top"

        self.required_frames.extend(
            [
                self.base_frame,
                self.sensor_kit_frame,
                self.source_frame,
                self.source_base_frame,
                self.target_frame,
            ]
        )

        self.add_calibrator(
            service_name="calibrate_lidar_lidar",
            expected_calibration_frames=[
                FramePair(parent=self.target_frame, child=self.source_frame),
            ],
        )

    def post_process(self, calibration_transforms: Dict[str, Dict[str, np.array]]):
        # Known from TF: sensor_kit_base_link -> velodyne_top
        sensor_kit_to_target = self.get_transform_matrix(
            self.sensor_kit_frame, self.target_frame
        )

        # Known from TF: velodyne_rear -> velodyne_rear_base_link
        source_to_source_base = self.get_transform_matrix(
            self.source_frame, self.source_base_frame
        )

        # Chain: sensor_kit -> velodyne_top @ velodyne_top -> velodyne_rear @ velodyne_rear -> velodyne_rear_base_link
        sensor_kit_to_source_base = (
            sensor_kit_to_target
            @ calibration_transforms[self.target_frame][self.source_frame]
            @ source_to_source_base
        )

        return {self.sensor_kit_frame: {self.source_base_frame: sensor_kit_to_source_base}}
