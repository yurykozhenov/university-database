from flask import (render_template, redirect, flash, request)
from peewee import CharField


def list_records(model, active_page, title="", record_id=None):
    if record_id:
        records = model.select().where(
            model.id == record_id
        )
    else:
        records = model.select()

        for key in request.args:
            if isinstance(getattr(model, key), CharField):
                records = records.where(
                    getattr(model, key) % request.args.get(key)
                )
            else:
                records = records.where(
                    getattr(model, key) % request.args.get(key)
                )

    return render_template('table.html',
                           records=records,
                           active_page=active_page,
                           title=title,
                           fields=model.fields)


def find_records(form_class, active_page, title=""):
    if request.method == "POST":
        query_list = []

        for key in request.form:
            if request.form[key] and key != 'csrf_token':
                query_list.append("{}={}".format(key, request.form[key]))

        query = "&&".join(query_list)

        return redirect('/{}?{}'.format(active_page, query))

    return render_template('search_form.html',
                           form=form_class(),
                           active_page=active_page,
                           title=title)


def new_record(model, form_class, active_page, title=""):
    form = form_class()

    if form.validate_on_submit():
        record = model()

        for attr in model.fields:
            if attr == "id":
                continue
            setattr(record, attr, getattr(form, attr).data)

        record.save()

        flash("Запис успішно створенний!", "success")
        return redirect('/{}'.format(active_page))

    return render_template('form.html',
                           form=form,
                           active_page=active_page,
                           title=title)


def edit_record(model, form_class, record_id, active_page, title=""):
    form = form_class()

    record = model.get(model.id == record_id)

    if form.validate_on_submit():
        for attr in model.fields:
            if attr == "id":
                continue
            setattr(record, attr, getattr(form, attr).data)

        record.save()

        flash("Запис {} успішно змінений!".format(
            record_id), "success")
        return redirect('/{}'.format(active_page))

    return render_template('form.html',
                           form=form,
                           record=record,
                           active_page=active_page,
                           title=title)


def delete_record(model, record_id, active_page):
    student = model.get(model.id == record_id)

    student.delete_instance()

    flash("Запис {} успішно видаленний!".format(
        record_id), "success")

    return redirect('/{}'.format(active_page))
