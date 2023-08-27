from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import UnsupportedMediaType

from mypass.db import utils as db_utils
from .com import IDENTITY_UID, IDENTITY_TOK

VaultApi = Blueprint('vault', __name__)


@VaultApi.route('/api/db/vault/add', methods=['POST'])
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


@VaultApi.route('/api/db/vault/select', methods=['POST'])
@jwt_required()
def vault_select():
    try:
        req = request.json
    except UnsupportedMediaType:
        req = {}
    identity = get_jwt_identity()
    username = req.get('username')
    password = req.get('password')
    title = req.get('title')
    website = req.get('website')
    notes = req.get('notes')
    folder = req.get('folder')
    entries = db_utils.select_vault_entry(identity[IDENTITY_UID])
    entries = db_utils.unlock_vault_entry(entries, enckey=identity[IDENTITY_TOK])
    return entries, 200


@VaultApi.route('/api/db/vault/update', methods=['POST'])
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


@VaultApi.route('/api/db/vault/delete', methods=['POST'])
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
