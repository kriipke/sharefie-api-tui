setup(
    name='sfapi',
    version='0.1.0',
    packages=find_packages(include=['sharefile_tui', 'sharefile_tui.*']),
    install_requires=[
        'rich'
    ]
    entry_points={
        'console_scripts': ['sfapi=sharefile-tui.tui:main']
    }
)
)
