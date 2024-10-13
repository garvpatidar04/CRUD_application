"""
This module deals with the voting process of the application

Author: Garv Patidar"""
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from app import models, database, oauth2, schemas
router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def voting(vote: schemas.Vote, db: Session =
        Depends(database.get_db), current_user:int = Depends(oauth2.get_current_user)):
    """
    This route allows users to vote on posts
    """
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=
            status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} was not found")

    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)

    vote_exist = vote_query.first()

    if vote.dir==1:
        if vote_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="You have already voted")
        new_vote = models.Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "your vote has been added successfully"}
    else:
        if not vote_exist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="you did not vote this post")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "you deleted your vote from the post"}
