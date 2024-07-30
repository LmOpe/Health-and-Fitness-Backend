from .settings import *

# Load environment variables from .env file
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)

# Local settings
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['https://fdh-inky.vercel.app/', 'https://fdh-lmos-projects.vercel.app/', 'localhost', '127.0.0.1', '.vercel.app', '.now.sh'])

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://fudhouse.vercel.app"
]