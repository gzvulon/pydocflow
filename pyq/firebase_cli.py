import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
# cred = credentials.ApplicationDefault()
cred = credentials.Certificate('/Users/ivanne/_ppp/darsearch-101dd20a5d22.json')

# firebase_admin.initialize_app(cred, {
#   'projectId': 'darsearch',
# })
firebase_admin.initialize_app(cred)
db = firestore.client()

col_ref = db.collection('test-sample')

doc_ref = col_ref.document(u'aturing')
doc_ref.set({
    u'first': u'Alan',
    u'middle': u'Mathison',
    u'last': u'Turing',
    u'born': 1912
})

docs = col_ref.stream()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

# https://firebase.google.com/docs/firestore/quickstart

