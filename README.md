# Project title

Marinero digital twin description files, controllers and localization logic.

## Getting started
Firstly, clone the repositroy with all the required dependencies.
Make sure that you have installed ROS2 packages: `ros2_control`, `controller_manager`, `twist_mux`, `joy` and `teleop_twist_joy`.

```
  cd workspace_folder
  git clone https://github.com/albic98/marinero_simulations.git
```

After cloning build the package in your `workspace_folder`. For example `marinero_ws`.

```
  source /opt/ros/<distro>/setup.bash
  colcon build --symlink-install
  source install/setup.bash
```

For the simulation to work, clone and build this two repositories in the same `workspace_folder`:
```
  git clone https://github.com/albic98/marinero_control.git
  source /opt/ros/<distro>/setup.bash
  colcon build --symlink-install
  source install/setup.bash
```

```
  git clone https://github.com/albic98/marinero_pointclouds.git
  source /opt/ros/<distro>/setup.bash
  colcon build --symlink-install
  source install/setup.bash
```

## Support

For support, email albert.androsic@fsb.unizg.hr.

Look at the README.md files of `marinero_control` and `marinero_pointclouds` for additional information.

## Usage/Examples

Start the robot state publisher for MARINERO:

```
  ros2 launch marinero_simulations rsp.launch.py
```

Initiate the entire simulation using this command (4WIS4WID controller) with `ros2_control.xacro`:
```
  ros2 launch marinero_simulations gazebo_simulation.launch.py
```

Launch command for controllers if they do not start with previous command:
```
  ros2 launch marinero_simulations controllers.launch.py
```

Initiate the entire simulation using this command (2 differential drive controller) with `gazebo_control.xacro`:
```
  ros2 launch marinero_simulations gazebo_simulation.launch.py use_ros2_control:=false use_4wis4wid:=false
```