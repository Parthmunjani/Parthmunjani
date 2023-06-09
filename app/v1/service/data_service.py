from app.models.model import *
from app.models.model import db
from app.models.model import *

class DataService:
    def __init__(self,model):
        self._model=model
        
    def get_all_data(self, id=None):
        if id is None:
            return [item.to_json() for item in self._model.query.all()]
        return [item.to_json() for item in self._model.query.filter_by(id=id).all()]
        """data = self._model.query.filter_by(id=id).first()
        
        if not data:
            return {}
        
        return data.to_json()"""
    
    def delete_data(self, id):
        item = self._model.query.get(id)
        if item:
            self._model.query.filter_by(id=id).delete()
            db.session.commit()
            return {"status": True, "detail": "Delete successfully"}
        else:
            return {"status": False, "detail": "Item not found"}

    def create_data(self, data):
        try:
            print(data)
            new_item = self._model(data)
            """db.session.add(new_item)
            db.session.commit()"""
            self._model.add(new_item)
            return {"status": True, "detail": "Data created successfully"}
        except Exception as e:
            return {"status": False, "detail": str(e)}
        
