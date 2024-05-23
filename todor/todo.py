from todor.auth import login_required
from flask import Blueprint, render_template, request, request, url_for, redirect, flash, session, g
from .models import Todo, User
from todor import db

bp = Blueprint('todo', __name__, url_prefix='/todo')


@bp.route('/list')
@login_required
def lista():
    todos = Todo.query.all()
    return render_template('todo/index.html', todos=todos)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(g.user.id, title, desc)

        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo.lista'))

    return render_template('todo/create.html')


def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def editar(id):

    todo = get_todo(id)

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.state = True if request.form.get('state') == 'on' else False

        db.session.commit()

        return redirect(url_for('todo.lista'))

    return render_template('todo/edit.html', todo=todo)


@bp.route('/delete/<int:id>', methods=('GET', 'POST'))
@login_required
def eliminar(id):
    todo = get_todo(id)
    if request.method == 'POST':
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('todo.lista'))
    return render_template('todo/delete.html', todo=todo)
