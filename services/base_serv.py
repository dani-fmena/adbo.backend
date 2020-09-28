from typing import Union
from fastapi import HTTPException, status
from api.utils.definitions import SDES
from bson.objectid import ObjectId, InvalidId


class BaseService:

    # Validation methods
    def chk_object_id(self, dto_id: str) -> Union[None, ObjectId]:
        """
        Try to check if the string representation param is an BSON ObjectID, if is ok then convert to ObjectId

        :param dto_id: BSON ObjectId string representation
        :return: ObjectId
        """
        try: object_id = ObjectId(dto_id)
        except InvalidId: self.RiseHTTP_BadRequest("The ID of the entity isn't valid.")
        else: return object_id

    # Exception methods
    def RiseHTTP_NotFound(self, details: str = SDES.NOTFOUND):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=details)

    def RiseHTTP_BadRequest(self, details: str = SDES.BADREQUEST):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=details)
