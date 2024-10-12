from fastapi import APIRouter

from .products.views import router as products_router

#добавляем router из файла views этот будет основным
router = APIRouter()
router.include_router(
    router=products_router,
      prefix="/products",
      )