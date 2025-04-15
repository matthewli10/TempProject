import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore    
from firebase_admin import auth
import uuid  

cred = credentials.Certificate("firebase_key.json") 
firebase_admin.initialize_app(cred)
db = firestore.client()

"""
For the user parameter, we need to create a function to store user id
"""
@app.post('/post')
async def post_on_app(
    title: str,
    gossip: str,
    user_id: str,
    date: str,
    time: str,
    image: str
) -> None:

    db = firestore.client()

    postId = str(uuid.uuid4())
    
    post_data = {
        "id": post, 
        "title" : title, 
        "gossip" : gossip,
        "user_id" : user.id,
        "date": date, 
        "time": time,
    }
    try:
        db.collection("posts").document(postId).set(post_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create post: {str(e)}"
        )

