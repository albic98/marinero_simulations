# MARINERO

Digital twin description files, controllers, and localization logic for the **MARINERO** robot in **ROS 2**.  
This package enables simulation of the robot in Gazebo and RViz, including both differential drive and 4WIS4WID control modes.

---

## Requirements  

- **ROS 2 Humble** (or compatible ROS 2 distribution)  
- Packages:  
  - `ros2_control`  
  - `controller_manager`  
  - `twist_mux`  
  - `joy`  
  - `teleop_twist_joy`
  - `gazebo`  

---

## Installation

Clone the repository in your ROS2 workspace.

```
  cd workspace_folder/src
  git clone https://github.com/albic98/marinero_simulations.git
```

After cloning build the package in your `workspace_folder/src`. For example `marinero_ws/src`.

```
  source /opt/ros/<distro>/setup.bash
  colcon build --symlink-install
  source install/setup.bash
```

For the simulation to work, clone and build the following repositories in the same `workspace_folder/src`:
```
  git clone https://github.com/albic98/marinero_control.git
  git clone https://github.com/albic98/marinero_pointclouds.git
```

Then build your workspace:
```
  source /opt/ros/<distro>/setup.bash
  colcon build --symlink-install
  source install/setup.bash
```

---

## Usage/Examples

#### Start the robot state publisher for MARINERO:

```
  ros2 launch marinero_simulations rsp.launch.py
```

#### Initiate the entire simulation using this command (4WIS4WID controller) with `ros2_control.xacro`:
```
  ros2 launch marinero_simulations gazebo_simulation.launch.py
```

#### Launch command for controllers if they do not start automatically:
```
  ros2 launch marinero_simulations controllers.launch.py
```

#### Initiate the entire simulation using this command (2 differential drive controller) with `gazebo_control.xacro`:
```
  ros2 launch marinero_simulations gazebo_simulation.launch.py use_ros2_control:=false use_4wis4wid:=false
```

---

## Support

For support, email albert.androsic@fsb.unizg.hr.

Look at the READMEs of `marinero_control` and `marinero_pointclouds` for additional information.