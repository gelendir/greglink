import os
from greglink import app

app.config.from_object('greglink.config.default_config')
app.config.from_envvar('CONFIG_FILE')

if __name__ == "__main__":
    port = int(app.config['PORT'])
    debug = int(app.config['DEBUG'])
    host = app.config['HOST']
    app.run(host=host, port=port, debug=debug)
