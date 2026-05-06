from app.extensions import db
from app.models.role import Role
from sqlalchemy import select
from .schemas import RoleResponseSchema
import traceback

class RoleService:
    @staticmethod
    def get_all_roles():
        try:
            roles = db.session.execute(select(Role)).scalars().all()
            return RoleResponseSchema(many=True).dump(roles)
        except Exception as ex:
            print(f"Hiba a szerepkorok lekerdezesenel: {ex}")
            return []

    @staticmethod
    def create_role(data):
        try:
            role = Role(**data)
            db.session.add(role)
            db.session.commit()
            return True, RoleResponseSchema().dump(role)
        except Exception as ex:
            db.session.rollback()
            print("HIBA A SZEREPKOR MENTESENEL:")
            traceback.print_exc()
            return False, str(ex)

    @staticmethod
    def delete_role(role_id):
        try:
            role = db.session.get(Role, role_id)
            if not role:
                return False, "Szerepkor nem talalhato"
            db.session.delete(role)
            db.session.commit()
            return True, "Szerepkor torolve"
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)