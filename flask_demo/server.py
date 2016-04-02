from app.base import app
from app.helpers.request import *
from app.models.comment import Comment
from app.models.item import Item

if __name__ == '__main__':
    port = 5000
    #print("RUN python app dirrectly on port %d" % port)
    app.run(debug=True)
