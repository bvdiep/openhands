module.exports = {
  apps: [{
    name: 'simple_web_cccd',
    script: '.venv/bin/python',
    args: 'app.py',
    cwd: '/home/diep/work/diep/openhands/apps/simple_web_cccd',
    interpreter: 'none',
    watch: false,
    instances: 1,
    exec_mode: 'fork',
    env: {
      PYTHONPATH: '/home/diep/work/diep/openhands/apps/simple_web_cccd',
      NODE_ENV: 'development',
    },
    out_file: 'logs/simple_web_cccd.log',
    error_file: 'logs/simple_web_cccd-error.log',
    merge_logs: true,
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    restart_delay: 10000, // 10 seconds between restarts
    max_memory_restart: '10G',
    env_file: '.env'
  }]
};