from setuptools import find_packages, setup

package_name = 'drone_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sean',
    maintainer_email='scsean19@gmail.com',
    description='Launch and initialization package for autonomous quadcopter system',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
		'camera_node = drone_bringup.camera_node:main',
        ],
    },
)
