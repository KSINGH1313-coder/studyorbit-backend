from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth
from routes.batch_routes import batch
from routes.notes_routes import notes
from flask import send_from_directory
from routes.attendance_routes import attendance
from routes.announcement_routes import announcement
from routes.assignment_routes import assignment
from routes.test_routes import test
app = Flask(__name__)

# 🔥 IMPORTANT FIX
CORS(app, resources={r"/*": {"origins": "*"}})

# register routes
app.register_blueprint(auth, url_prefix="/api")
app.register_blueprint(batch, url_prefix="/api/batch")
app.register_blueprint(notes, url_prefix="/api/notes")

app.register_blueprint(attendance, url_prefix="/api/attendance")

app.register_blueprint(announcement, url_prefix="/api/announcement")

app.register_blueprint(assignment, url_prefix="/api/assignment")

app.register_blueprint(test, url_prefix="/api/test")
@app.route("/")
def home():
    return {"message": "Backend Running 🚀"}
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == "__main__":
    app.run(debug=True)