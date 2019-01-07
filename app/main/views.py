from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from datetime import datetime
from forms import MemoForm, LatLngForm
from ..models import User,Memo
from .. import db
from . import main


@main.route('/')
def index():
    return render_template('index.html',current_time=datetime.utcnow())

@main.route('/user/<username>', methods=['GET','POST'])
@login_required
def user(username):
    form = MemoForm()
    if form.validate_on_submit():
        memo = Memo(title=form.title.data, body=form.body.data, time=form.time.data, owner=current_user._get_current_object(), placename=None, lat=0.0, lng=0.0)
        db.session.add(memo)
        db.session.commit()
        return redirect(url_for('.user',username=username))
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    memos = user.memos.order_by(Memo.time.desc()).all()
    return render_template('usercenter.html', form=form ,memos=memos )


@main.route('/edit/<int:memo_id>',methods=['GET','POST'])
@login_required
def edit(memo_id):
    memo=Memo.query.filter_by(id=memo_id).first()
    form = MemoForm()
    if form.validate_on_submit():
        memo.title = form.title.data
        memo.body = form.body.data      
        memo.time = form.time.data  
        db.session.add(memo)
        db.session.commit()
        flash("Updated Successfully")
        return redirect(url_for('.user',username=current_user.username))  
        flash("Redirect UN Successfully")     
    form.title.data = memo.title
    form.body.data = memo.body
    form.time.data = memo.time
    return render_template('edit_memo.html', form=form)


@main.route('/delete/<int:memo_id>')
@login_required
def delete_memo(memo_id):
    memo=Memo.query.filter_by(id=memo_id).first()
    db.session.delete(memo)
    db.session.commit()
    flash("Deleted Successfully")
    return redirect(url_for('.user',username=current_user.username))  


@main.route('/maptest')
def maptest():
    latlngform = LatLngForm()
    return render_template('edit_latlng.html', form=latlngform)


@main.route('/edit_latlng/<int:memo_id>',methods=['GET','POST'])
@login_required
def edit_latlng(memo_id):
    form = LatLngForm()
    memo=Memo.query.filter_by(id=memo_id).first()
    if form.validate_on_submit():
        memo.placename = form.placename.data
        memo.lat = form.lat.data      
        memo.lng = form.lng.data  
        db.session.add(memo)
        db.session.commit()
        flash("Updated Successfully")
        return redirect(url_for('.user',username=current_user.username))  
    form.placename.data = memo.placename
    form.lat.data = memo.lat
    form.lng.data = memo.lng
    return render_template('edit_latlng.html', form=form)





