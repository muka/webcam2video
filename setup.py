from setuptools import setup

setup(
    name='webcam2video',
    version='1.0.0',
    description='save webcam and mjpeg stream to video',
    long_description='',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
        ],
    url='https://github.com/muka/webcam2video',
    author='Luca Capra',
    author_email='luca.capra@gmail.com',
    license='MIT',
    packages=['webcam', 'mjpeg', 'video', 'cv2', 'opencv'],
    zip_safe=True,
)
