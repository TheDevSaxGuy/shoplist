import firebase_admin 
from firebase_admin import credentials
from firebase_admin import firestore

credential= credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()

def get_users():
  return db.collection('users').get()

def get_products(user_id):
  return db.collection('users').document(user_id).collection('compras').get()

def get_total(user_id):
  precios = []
  products = db.collection('users').document(user_id).collection('compras').get()
  for product in products:
    precios.append(product.to_dict()['precio'])
  total = sum(precios)
  return total

def get_user(user_id):
  return db.collection('users').document(user_id).get()

def user_put(user_data):
  user_ref = db.collection('users').document(user_data.username)
  user_ref.set({'password': user_data.password})

def put_product(user_id, description, price):
  product_collection_ref = db.collection('users').document(user_id).collection('compras')
  product_collection_ref.add({'descripcion' : description, 'precio': price, 'done': False})

def delete_product(user_id, product_id):
  product_ref = _get_product_ref(user_id, product_id)
  product_ref.delete()

def put_capital(user_id, capital):
  product_collection_ref = db.collection('users').document(user_id).document('capital')
  product_collection_ref.set({'capital':capital})

def get_capital(user_id):
  return db.collection('users').document(user_id).get()

def update_product(user_id, product_id, done):
  product_done = bool(done)
  product_ref = _get_product_ref(user_id, product_id)
  product_ref.update({'done': not product_done})


def _get_product_ref(user_id, product_id):
  return db.document('users/{}/compras/{}'.format(user_id, product_id))