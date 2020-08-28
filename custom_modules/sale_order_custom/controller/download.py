import logging
try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO
import zipfile
from datetime import datetime
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition
import ast
import json

_logger = logging.getLogger(__name__)


class DownloadMultipleFiles(http.Controller):
    @http.route('/web/binary/download_document', type='http', auth="user")
    def download_document(self, product_ids, type, **kw):
        product_ids = json.loads(product_ids)
        attachment_ids = request.env['ir.attachment'].search(['&',('res_model','=','product.template'),('res_id', 'in', product_ids)])
        file_dict = {}
        for attachment_id in attachment_ids:
            file_name = attachment_id.name.replace(".pdf","")
            if (type == "ficha_ESP"):
                if(len(file_name) > 2 and file_name.startswith('2')):
                    file_store = attachment_id.store_fname
                    if file_store:
                        file_name = attachment_id.name
                        file_path = attachment_id._full_path(file_store)
                        file_dict["%s:%s" % (file_store, file_name)] = dict(path=file_path, name=file_name)    
            elif (type == "ficha_EN"):
                if(len(file_name) == 2):
                    file_store = attachment_id.store_fname
                    if file_store:
                        file_name = attachment_id.name
                        file_path = attachment_id._full_path(file_store)
                        file_dict["%s:%s" % (file_store, file_name)] = dict(path=file_path, name=file_name)    
            elif (type == "Cert"):
                if(len(file_name) > 2 and file_name.startswith('1')):
                    file_store = attachment_id.store_fname
                    if file_store:
                        file_name = attachment_id.name
                        file_path = attachment_id._full_path(file_store)
                        file_dict["%s:%s" % (file_store, file_name)] = dict(path=file_path, name=file_name)
        zip_filename = datetime.now()
        zip_filename = "%s.zip" % zip_filename
        bitIO = BytesIO()
        zip_file = zipfile.ZipFile(bitIO, "w", zipfile.ZIP_DEFLATED)
        for file_info in file_dict.values():
            zip_file.write(file_info["path"], file_info["name"])
        zip_file.close()
        return request.make_response(bitIO.getvalue(),
                                     headers=[('Content-Type', 'application/x-zip-compressed'),
                                              ('Content-Disposition', content_disposition(zip_filename))])

