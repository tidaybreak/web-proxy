#!env python
# coding=utf-8


from app.config import cfg
from app.settings import create_app, configure_blueprints
app = create_app(conf=cfg)

import app.routers as routers
app = configure_blueprints(app, routers.MOUNT_POINTS)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=cfg.PORT)
