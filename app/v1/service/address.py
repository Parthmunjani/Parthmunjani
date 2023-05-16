from app.models.model import UserAddressModel
from datetime import datetime

class AddressService:
    def get_all_addresses():
        try:
            addresses = UserAddressModel.query.all()
            if not addresses:
                return {"status": False, "detail": "Address Not found"}
            data = [address.to_json() for address in addresses]
            return {"status": True, "detail": data}
        except Exception as e:
            return {"status": False, "details": str(e)}

    def create_address(data):
        try:
            create_user_address = UserAddressModel(data)
            UserAddressModel.add(create_user_address)
            data = create_user_address.to_json()
            return {"status": True, "detail": "User Address Add Successfully"}
        except Exception as e:
            return {"status": False, "detail": str(e)}

    def get_address_by_id(id):
        try:
            address = UserAddressModel.query.get(id)
            if not address:
                return {"status": False, "details": "Address Not found"}
            data = address.to_json()
            return {"status": True, "detail": data}
        except Exception as e:
            return {"status": False, "detail": str(e)}

    def update_address(id, data):
        try:
            address = UserAddressModel.query.get(id)
            if not address:
                return {"status": False, "details": "Address Not found"}
            address.state = data.get('state')
            address.street = data.get('street')
            address.user_id = data.get('user_id')
            address.zip = data.get('zip')
            address.modified_at = datetime.utcnow()
            UserAddressModel.put()
            data = address.to_json()
            return {"status": True, "detail": data}
        except Exception as e:
            return {"status": False, "detail": str(e)}

    def delete_address(id):
        try:
            address = UserAddressModel.query.get_or_404(id)
            UserAddressModel.delete(address)
            return {"status": True, "detail": "Address Delete"}
        except Exception as e:
            return {"status": False, "detail": str(e)}
