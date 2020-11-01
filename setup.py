from setuptools import setup

APP = ['main.py']
APP_NAME = "Minimalio"
DATA_FILES = [
    ('Application/static', ['Application/static/favicorn.png', 
            'Application/static/favicon.png', 
            'Application/static/Evogria.otf',
            'Application/static/Delvon.ttf',
            ]
    ),
]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'Application/static/minimalio_icon.icns',
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=[
        'py2app',
        'pygame'
        ],
)
