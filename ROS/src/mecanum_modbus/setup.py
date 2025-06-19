from setuptools import setup

package_name = 'mecanum_modbus'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    py_modules=['mecanum_modbus_controller'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Chetan Shinde',
    maintainer_email='shindechetan.ttd@gmail.com',
    description='ROS 2 node to control RMCS-3001 motor drivers using pymodbus and /cmd_vel',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mecanum_modbus_controller = mecanum_modbus_controller:main',
        ],
    },
)