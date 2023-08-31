from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from mypass.db import utils as db_utils
from mypass.models import VaultEntry
from .com import IDENTITY_UID, IDENTITY_TOK

VaultApi = Blueprint('vault', __name__)


@VaultApi.route('/api/db/vault/add', methods=['POST'])
@jwt_required()
def vault_add():
    req = request.json
    fields = req.get('fields', {})
    entry = db_utils.insert_vault_entry(**fields)
    return {'id': entry.id}, 200


@VaultApi.route('/api/db/vault/select', methods=['POST'])
@jwt_required()
def vault_select():
    req = request.json
    crit = req.get('crit', {})
    identity = get_jwt_identity()
    crit['user_id'] = identity[IDENTITY_UID]
    crit['active'] = True
    crit['deleted'] = False
    entries = db_utils.select_vault_entry(**crit)
    entries = db_utils.unlock_vault_entry(entries, enckey=identity[IDENTITY_TOK])
    return entries, 200


@VaultApi.route('/api/db/vault/update', methods=['POST'])
@jwt_required()
def vault_update():
    req = request.json
    crit = req.get('crit', {})
    fields = req.get('fields', {})
    fields = {f'new_{k}': fields[k] for k in fields}
    identity = get_jwt_identity()
    crit['user_id'] = identity[IDENTITY_UID]
    crit['active'] = True
    crit['deleted'] = False
    updates = db_utils.update_vault_entry(**crit, **fields)
    return {'affected_rows': updates}, 200


@VaultApi.route('/api/db/vault/delete', methods=['POST'])
@jwt_required()
def vault_delete():
    req = request.json
    req_crit = req.get('crit', {})
    identity = get_jwt_identity()
    crit = VaultEntry.map_criterion(crit=req_crit)
    crit['user_id'] = identity[IDENTITY_UID]
    crit['active'] = True
    crit['deleted'] = False
    deletes = db_utils.delete_vault_entry(**crit)
    return {'affected_rows': deletes}, 200
