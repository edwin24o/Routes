from app.extensions import ma
from app.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# class RatingSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Rating
#         include_fk = True

# rating_schema = RatingSchema()
# ratings_schema = RatingSchema(many=True)

# class MessageSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Message
#         include_fk = True

# message_schema = MessageSchema()
# messages_schema = MessageSchema(many=True)