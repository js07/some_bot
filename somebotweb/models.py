import time

from flask import url_for

from somebotweb import db

class User(db.Model):
    __tablename__ = 'users'  # 'user' is special in postgres
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Reconsider using Text and instead use String?  Probably some performance differences and ability to index blah blah blah
    name = db.Column(db.Text)
    email = db.Column(db.Text)

    def __init__(self, name, email):
        self.name = name
        self.email = email


class Map(db.Model):
    # TODO: package instead of module
    # TODO: nicer docstrings
    '''
    The map schema
    To make a map, we need a mapname, and author, and a description
    times_tested, last_tested and upload_time are generated when a map
    object is created
    '''

    id = db.Column(db.Integer, primary_key=True)

    # TODO: make sure mapname gets indexed
    mapname = db.Column(db.Text)
    author = db.Column(db.Text)
    description = db.Column(db.Text)
    upload_time = db.Column(db.Float)
    # TODO: sql alchemdy doesn't have some date type?
    last_tested = db.Column(db.Float)
    times_tested = db.Column(db.Integer)
    status = db.Column(db.Text)

    def __init__(self, mapname, author, description, status=None, upload_time=None):
        self.mapname = mapname
        self.author = author
        self.description = description
        self.upload_time = upload_time or time.time()
        self.last_tested = 0
        self.times_tested = 0
        self.status = status

    def __repr__(self):
        return "<Map [%s] %s - %s>" %(str(self.id), self.mapname, self.author)

    def get_json(self):
        # TODO: this just returns a python dict, not json :/
        '''
        Input: map from database - given by Map class from sqlalchemy
        Output: Map formatted in JSON
        '''
        strid = str(self.id)

        map_data = {
            'mapid': self.id,
            'mapname': self.mapname,
            'author': self.author,
            'description': self.description,
            'status': self.status,
            'jsonurl': "/static/maps/"+strid+'.json',
            'uploaddate': time.strftime('%Y-%m-%d', time.localtime(self.upload_time)),
            'pngurl': "/static/maps/"+strid+'.png',
            'previewurl': "/static/previews/"+strid+'.png',
            'thumburl': "/static/thumbs/"+strid+'.png',
            'times_tested': self.times_tested,
            "mapurl": "/show/"+strid,
            "authorurl": url_for('return_maps_by_author', author=self.author),
            # TODO:  why mapname in here?
            # TODO: it's to name the downloaded file; we should move to
            # storing the files in directories (with name id) and then
            # keeping nice names inside.
            "pngdownload": u"/download?mapname={mapname}&type=png&mapid={mapid}".format(mapname=self.mapname, mapid=strid),
            "jsondownload": u"/download?mapname={mapname}&type=json&mapid={mapid}".format(mapname=self.mapname, mapid=strid),
            }
        return map_data


db.Index('mapname_idx', db.func.lower(Map.mapname))
db.Index('mapname_trgm_idx', Map.mapname, postgresql_ops={'mapname': 'gist_trgm_ops'}, postgresql_using="gist")
