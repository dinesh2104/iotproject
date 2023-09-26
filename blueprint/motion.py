from flask import Flask,render_template,session,request,redirect,url_for,Blueprint
from src.User import User
from gridfs import GridFS,GridFSBucket
import mimetypes
import uuid
from src.Database import Database

bp=Blueprint("motion",__name__,url_prefix="/api/motion")

@bp.route("/capture",methods=['POST'])
def capture_motion():
    if 'file' in request.files and session.get('authenticated'):
      file=request.files['file']
      fs=GridFSBucket(Database.get_connection())
      metadata={
        'original_filename':file.filename,
        'content_type': mimetypes.guess_type(file.filename)[0],
        'owner':session.get('username')
      }

      filename=str(uuid.uuid4())
      file_id=fs.upload_from_stream(filename,file,metadata=metadata)

      return {
        'message':"Upload Success",
        'file_id':str(file_id),
        'filename':filename,
        'download_url':"/files/get/bucket/"+filename,
        'type':'correct'
      },200  
    else:
        return {
            "message": " Bad Request",
            'type':"error"
        },400