from flask_restful import Resource
from flask import make_response,request
from model import UserAddressModel
from datetime import datetime

class AddressView(Resource):
    def get(self):
        try:
            address = UserAddressModel.query.all()
            if not address:
                return make_response({"status":False,"detail":"Any Address Not in Data"})
            data = [user.to_json(user) for user in address]
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"details":str(e)})
            
    def post(self):
        try:
            data=request.get_json()
            create_user = UserAddressModel(data)
            UserAddressModel.add(create_user)
            data=create_user.to_json(create_user)
            return make_response({"status":True,"detail":"User Address Add Successfully"})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
    
class Addressdetails(Resource):
    def get(self,id):
        try:
            address = UserAddressModel.query.get(id) 
            if not address:
                return make_response({"status": False, "details": "Address Not In Data"})
            data=address.to_json(address)
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
    def put(self,id):
        try:
            address=UserAddressModel.query.get(id)
            data=request.get_json()
            address.state = data.get('state')
            address.street = data.get('street')
            address.user_id=data.get('user_id')
            address.zip=data.get('zip')
            address.modified_at=datetime.utcnow()
            UserAddressModel.put()
            data=address.to_json(address)
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
    def delete(self,id):
        try:
            address = UserAddressModel.query.get_or_404(id)
            UserAddressModel.delete(address)
            return make_response({"Status":True,"detail":"User Data Delete"})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})