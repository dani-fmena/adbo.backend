from fastapi import HTTPException, status
from api.utils.definitions import SDES


class BaseService:

    def RiseHTTP_NotFound(self, details: str = SDES.NOTFOUND):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)
