from flask import Blueprint ,render_template ,request ,g ,redirect ,url_for
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db


bp = Blueprint('qa', __name__, url_prefix='/')

@bp.route('/')
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('index.html', questions=questions)


@bp.route('/qa/public', methods=['GET', 'POST'])
def public_qa():
    if request.method == 'GET':
        if not g.user:
            return redirect('/auth/login')
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()

            return redirect("/")

        else:
            print(form.errors)
            return "发布错误，请检查内容"

@bp.route("/qa/detail/<qa_id>")
def detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template('detail.html', question=question)

@bp.route("/qa/answer/public", methods=['POST'])
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(question_id=question_id, content=content, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('qa.detail', qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for('qa.detail', qa_id=request.form.get("question_id")))


@bp.route("/search")
def search():
    q = request.args.get('q')
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    if q:
        return render_template("index.html", questions=questions)
    else:
        return redirect(url_for('qa.index'))

@bp.route("/qa/delete", methods=['POST'])
def delete():
    user_id = request.form.get("user_id")
    a_id =g.user.id
    if str(a_id) == str(user_id):
        answer_id = request.form['answer_id']
        answer = AnswerModel.query.get(answer_id)
        db.session.delete(answer)
        db.session.commit()
        return redirect(url_for('qa.detail', qa_id=request.form.get("question_id")))
    else:
        return redirect(url_for('qa.detail', qa_id=request.form.get("question_id")))

@bp.route("/qa/q/delete", methods=['POST'])
def q_delete():
    user_id = request.form.get("user_id")
    a_id =g.user.id
    if str(a_id) == str(user_id):
        question_id = request.form['question_id']
        question = QuestionModel.query.get(question_id)
        db.session.delete(question)
        db.session.commit()
        null_answers = AnswerModel.query.filter(None).all()
        print(null_answers)

        for null_answer in null_answers:
            db.session.delete(null_answer)
            db.session.commit()
        return redirect("/")
    else:
        return redirect("/")




