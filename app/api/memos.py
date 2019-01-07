from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Memo
from . import api
from .errors import forbidden


@api.route('/memos/')
def get_all_memo():
    memos = Memo.query.filter_by(user_id=g.current_user.id).all()
    return jsonify({  'memos:': [memo.to_json() for memo in memos] })


@api.route('/memos/<int:id>')
def get_memo(id):
    memo = Memo.query.filter_by(id=id).first()
    if memo is None:
        abort(404)
    if memo.user_id != g.current_user.id:
        return forbidden("You Cannot Access Other's Memos")
    return jsonify(memo.to_json())


@api.route('/memos/', methods=['POST'])
def add_memo():
    memo = Memo.from_json(request.json)
    memo.owner = g.current_user
    db.session.add(memo)
    db.session.commit()
    return jsonify(memo.to_json()), 201, \
        {'Location': url_for('api.get_memo', id=memo.id)}


@api.route('/memos/<int:id>', methods=['PUT'])
def edit_memo(id):
    memo = Memo.query.filter_by(id=id).first()
    if memo is None:
        abort(404)
    if memo.user_id != g.current_user.id:
        return forbidden("You Cannot Access Other's Memos")
    memo.body = request.json.get('body', memo.body)
    if request.json.get('time') is not None:
        memo.time = request.json.get('time')  
    if request.json.get('title') is not None:
        memo.title = request.json.get('title')  
    db.session.add(memo)
    db.session.commit()
    return jsonify(memo.to_json())
