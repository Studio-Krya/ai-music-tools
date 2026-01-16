from .app.router import router
from .core.setup import create_application

app = create_application(router=router)