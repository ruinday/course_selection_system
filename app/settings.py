TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': 'localhost',
                'port': '3306',
                'user': 'root',
                'password': 'mm546896',
                'database': 'courses_selection_system',
                'minsize': 1,
                'maxsize': 5,
                'charset': 'utf8mb4'
            }
        }
    },
    'apps': {
        'models': {
            'models': ['aerich.models', "models"],  # aerich.models是用于迁移的模型
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}