# Deployment Guide

## Local Development

### Prerequisites
- Python 3.9+
- pip or conda
- Git

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/real-estate-analyzer.git
   cd real-estate-analyzer
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the application:**
   ```bash
   python -m flask run
   ```

The app will be available at `http://localhost:5000`

## Docker Deployment

### Build and Run with Docker

```bash
docker build -t real-estate-analyzer .
docker run -p 5000:5000 real-estate-analyzer
```

### Docker Compose

```bash
docker-compose up
```

## Production Deployment

### Using Gunicorn

1. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 "src.app:create_app()"
   ```

### Using systemd (Linux)

1. **Create service file:**
   ```bash
   sudo nano /etc/systemd/system/real-estate-analyzer.service
   ```

2. **Add configuration:**
   ```ini
   [Unit]
   Description=Real Estate Market Analyzer
   After=network.target

   [Service]
   Type=notify
   User=www-data
   WorkingDirectory=/opt/real-estate-analyzer
   ExecStart=/opt/real-estate-analyzer/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 "src.app:create_app()"
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start:**
   ```bash
   sudo systemctl enable real-estate-analyzer
   sudo systemctl start real-estate-analyzer
   ```

### Environment Variables

Key environment variables for production:

```
FLASK_ENV=production
SECRET_KEY=<long-random-string>
DATABASE_URL=postgresql://user:pass@localhost/real_estate
```

## Database Migrations

Initial setup:
```bash
python -c "from src.app import create_app; app = create_app(); app.app_context().push()"
```

## Monitoring

- Use tools like PM2, Supervisor, or systemd for process management
- Set up logging to files and external services
- Monitor database performance
- Track API response times

## Backup

Regular database backups are essential:

```bash
# SQLite
cp real_estate.db real_estate.db.backup

# PostgreSQL
pg_dump real_estate > backup.sql
```

## Security

- Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- Use HTTPS in production
- Set strong SECRET_KEY
- Validate and sanitize all user inputs
- Use environment variables for sensitive data
- Enable CSRF protection
