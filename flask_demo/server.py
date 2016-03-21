from app.base import app
from app.helpers.request import *
from app.models.comment import Comment
from app.models.item import Item

if __name__ == '__main__':
    debug = False
    port = 7000
    #print("RUN python app dirrectly on port %d" % port)
    app.run(host="0.0.0.0", port=port, debug=debug)
