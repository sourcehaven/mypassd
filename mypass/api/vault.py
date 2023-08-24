from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from mypass.db import utils as db_utils

VaultApi = Blueprint('auth', __name__)


@VaultApi.route('/api/vault/add', methods=['POST'])
@jwt_required()
def vault_add():
    req = request.json
    username = req.get('username')
    password = req.get('password')
    title = req.get('title')
    website = req.get('website')
    notes = req.get('notes')
    folder = req.get('folder')
    entry = db_utils.insert_vault_entry(
        username=username, password=password, title=title, website=website, notes=notes, folder=folder)
    return {'id': entry.id}, 200


@VaultApi.route('/api/vault/select', methods=['POST'])
@jwt_required()
def vault_select():
    req = request.json
    username = req.get('username')
    password = req.get('password')
    title = req.get('title')
    website = req.get('website')
    notes = req.get('notes')
    folder = req.get('folder')
    entries = db_utils.select_vault_entry()
    # TODO: convert entries to json serializable, or make serializer for model classes
    return entries, 200


@VaultApi.route('/api/vault/update', methods=['POST'])
@jwt_required()
def vault_update():
    req = request.json
    username = req.get('username')
    password = req.get('password')
    title = req.get('title')
    website = req.get('website')
    notes = req.get('notes')
    folder = req.get('folder')
    updates = db_utils.update_vault_entry()
    # TODO: create a meaningful update return statement
    return updates, 200


@VaultApi.route('/api/vault/delete', methods=['POST'])
@jwt_required()
def vault_delete():
    req = request.json
    username = req.get('username')
    password = req.get('password')
    title = req.get('title')
    website = req.get('website')
    notes = req.get('notes')
    folder = req.get('folder')
    deletes = db_utils.delete_vault_entry()
    # TODO: create a meaningful delete return statement
    return deletes, 200
