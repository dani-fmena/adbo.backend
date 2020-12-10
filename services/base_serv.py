from typing import Union, List, Final
from fastapi import HTTPException, status
from api.utils.definition_data import SDES, RESPHEADER
from bson.objectid import ObjectId


class BaseService:
    invalid_id_error_info: Final[str] = 'The ID of the entity isn\'t valid.'

    # Validation methods
    def chk_object_id(self, dto_id: str) -> Union[None, ObjectId]:
        """
        Try to check if the string representation param is an BSON ObjectID, if is ok then convert to ObjectId

        :param dto_id: String representation BSON ObjectId
        :return: ObjectId
        """
        try: object_id = ObjectId(dto_id)
        # except InvalidId: self.RiseHTTP_BadRequest(self.invalid_id_error_info)
        except: self.RiseHTTP_BadRequest(self.invalid_id_error_info)
        else: return object_id

    def chk_object_ids_list(self, dto_ids: List[str]) -> Union[None, List[ObjectId]]:
        """
        Try to check if the string representation for each item of param is an BSON ObjectID.
        If is ok then convert to list of ObjectId

        :param dto_ids: List string representation of BSON ObjectId
        :return: List of ObjectId
        """
        bson_list: List[ObjectId] = []

        for str_id in dto_ids:
            try: object_id = ObjectId(str_id)
            # except InvalidId: self.RiseHTTP_BadRequest(self.invalid_id_error_info)
            except: self.RiseHTTP_BadRequest(self.invalid_id_error_info)
            else: bson_list.append(object_id)

        return bson_list

    # Exception methods
    @staticmethod
    def RiseHTTP_NotFound(details: str = SDES.NOTFOUND):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = details)

    @staticmethod
    def RaiseHTTP_Unauthorized(details: str = SDES.UNAUTHORIZED, is_gen_auth_tk: bool = False):
        """
        Rise an unauthorized HTTP exception with the WWW-Authenticate header

        :param details: Custom string for the details of the HTTP exception
        :param is_gen_auth_tk: If the exception was trying to generate access token or accessing a resource (otherwise)
        :return:
        """
        headers = RESPHEADER.UNAUTHORIZED_BEARER if is_gen_auth_tk else RESPHEADER.UNAUTHORIZED_RESOURCE
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = details, headers = headers)

    @staticmethod
    def RiseHTTP_BadRequest(details: str = SDES.BAD_REQUEST):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = details)

    @staticmethod
    def RiseHTTP_DalEmptyOps( details: str = SDES.DAL_FAIL_EMPTY):
        raise HTTPException(status_code = status.HTTP_417_EXPECTATION_FAILED, detail = details)

    @staticmethod
    def RiseHTTP_DataLayerFail( details: str = SDES.DAL_FAIL):
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = details)
