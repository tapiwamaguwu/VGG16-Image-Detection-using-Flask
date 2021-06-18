from flask import Flask,render_template,request,flash,redirect, url_for
import os
import model
from werkzeug.utils import redirect, secure_filename


# Create flask app
app = Flask(__name__)
# for encrypting the session
app.secret_key = "secret key" 
#setting Uploads Folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
#Setting allowed extensions (i.e. to allow for videos only)
ALLOWED_EXTENSIONS ={"mp4","avi","mkv"} 
#Uploads of up to 10Mbs only
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/" )
def hello():
    return render_template("index.html")

 #route to accept the video file 
@app.route("/submit", methods = ["POST","GET"])
def submit():
    if request.method=="POST":
        #Checking if user submitted an object to query
        if request.form['search'] =="":
            flash("Please enter search query")
            return redirect(request.url)
        #Checking if request has a file part
        if 'video' not in request.files:
            flash("No file part")
            return redirect(request.url)
        #Getting submitted file    
        file = request.files['video'] 
        #Checking if user submitted a file (The browser submits an empty file with no filename if the user doesn't select a file)
        if file.filename =="":
            flash("No selected file")
            return redirect(request.url)

        search_query=request.form['search']    
        #checking if file has the allowed extension
        if file and allowed_file(file.filename):
            #cleaning up the filename and making sure if doesn't cause any dangerous operations in the server's file directory
            filename = secure_filename (file.filename)
            #saving file to uploads folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #loading video into model
            flash('Processing submitted video',"submission")
            objects_found=model.predict('uploads/'+filename)
            isfound,query_results=search_for_object(search_query,objects_found)
            #return redirect(url_for('download_file',name=filename))
            return  render_template("submission.html",n={"search_query":search_query,"filename":filename,"isfound":isfound,"query_results":query_results})
        
        #else if file type not allowed
        flash("File Type Not Allowed. \".mp4\",\".avi\",\".mkv\" only")
        return redirect(request.url)
     #TODO If user goes straight to /submit   
    return render_template("submission.html",n="Nothing")    


def search_for_object(query,objects_found):
    isfound=False
    query_results=[]
    for object in objects_found:
        if query in object['prediction']:
            isfound=True
            query_results.append(object)

    return isfound,query_results    

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True,threaded=True)