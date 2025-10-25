from flask import Flask, flash, redirect, url_for, render_template, request, send_file, session
import os
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)
app.secret_key = "mysecretkey123"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 
    'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'zip', 'rar', 'mp3', 'mp4'
}

# File type categories
FILE_CATEGORIES = {
    'image': ['png', 'jpg', 'jpeg', 'gif', 'bmp'],
    'document': ['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'],
    'archive': ['zip', 'rar'],
    'video': ['mp4'],
    'audio': ['mp3']
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_category(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return 'other'

def get_file_icon(filename):
    category = get_file_category(filename)
    icons = {
        'image': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>',
        'document': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></svg>',
        'archive': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="21,8 21,21 3,21 3,8"/><rect x="1" y="3" width="22" height="5"/><line x1="10" y1="12" x2="14" y2="12"/></svg>',
        'video': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="23,7 16,12 23,17 23,7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>',
        'audio': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>'
    }
    return icons.get(category, '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></svg>')

def get_folder_contents(path):
    """Get files and folders in a given path"""
    items = []
    
    try:
        # Ensure path exists
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            is_directory = os.path.isdir(item_path)
            
            if is_directory:
                # It's a folder
                try:
                    item_count = len(os.listdir(item_path))
                except:
                    item_count = 0
                    
                items.append({
                    'name': item,
                    'type': 'folder',
                    'icon': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>',
                    'size': '-',
                    'item_count': item_count,
                    'path': item_path
                })
            else:
                # It's a file
                try:
                    file_size = os.path.getsize(item_path)
                except:
                    file_size = 0
                    
                file_category = get_file_category(item)
                file_icon = get_file_icon(item)
                
                items.append({
                    'name': item,
                    'type': 'file',
                    'icon': file_icon,
                    'size': file_size,
                    'category': file_category,
                    'path': item_path
                })
    except Exception as e:
        flash(f'Error reading directory: {str(e)}', 'error')
    
    # Sort: folders first, then files
    items.sort(key=lambda x: (x['type'] != 'folder', x['name'].lower()))
    return items

def get_breadcrumbs(current_path):
    """Generate breadcrumb navigation"""
    breadcrumbs = [{'name': 'Home', 'path': ''}]
    
    if current_path:
        parts = current_path.split('/')
        current_breadcrumb_path = ''
        
        for part in parts:
            if part:  # Skip empty parts
                current_breadcrumb_path = current_breadcrumb_path + '/' + part if current_breadcrumb_path else part
                breadcrumbs.append({
                    'name': part,
                    'path': current_breadcrumb_path
                })
    
    return breadcrumbs

# Create uploads folder if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Simple user database
users = {
    "hadjhassinejawher": "ChangeIt"
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username.strip() or not password.strip():
            flash('Please enter both username and password!', 'error')
            return redirect(url_for('login'))
        elif username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('files'))
        else:
            flash('Wrong username or password!', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/files', methods=['GET', 'POST'], defaults={'folder_path': ''})
@app.route('/files/<path:folder_path>', methods=['GET', 'POST'])
def files(folder_path):
    # Build current path safely
    current_path = os.path.join('uploads', folder_path)
    
    # Ensure path is within uploads directory and exists
    if not os.path.exists(current_path):
        try:
            os.makedirs(current_path, exist_ok=True)
        except Exception as e:
            flash(f'Error creating directory!', 'error')
            return redirect(url_for('files'))
    
    # Handle POST requests (file uploads and folder creation)
    if request.method == 'POST':
        # Handle folder creation
        if 'new_folder_name' in request.form:
            new_folder_name = secure_filename(request.form['new_folder_name'].strip())
            if new_folder_name:
                new_folder_path = os.path.join(current_path, new_folder_name)
                try:
                    os.makedirs(new_folder_path, exist_ok=True)
                    flash(f'Folder created successfully!', 'success')
                except Exception as e:
                    flash(f'Error creating folder!', 'error')
            else:
                flash('Please enter a valid folder name!', 'error')
            return redirect(url_for('files', folder_path=folder_path))
        
        # Handle file upload
        elif 'files' in request.files:
            files = request.files.getlist('files')
            uploaded_count = 0
            
            for file in files:
                if file.filename == '':
                    continue
                    
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    try:
                        file.save(os.path.join(current_path, filename))
                        uploaded_count += 1
                    except Exception as e:
                        flash(f'Error saving file!', 'error')
                else:
                    flash('Type not supported!', 'error')
            
            if uploaded_count > 0:
                flash(f'Files uploaded successfully!', 'success')
            return redirect(url_for('files', folder_path=folder_path))
    
    # Get items in current directory
    items = get_folder_contents(current_path)
    breadcrumbs = get_breadcrumbs(folder_path)
    
    username = session.get('username')
    
    return render_template('files.html', 
                         items=items, 
                         current_path=folder_path,
                         breadcrumbs=breadcrumbs,
                         username=username,
                         allowed_extensions=list(ALLOWED_EXTENSIONS))

@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_path = request.form.get('current_path', '')
    new_folder_name = secure_filename(request.form.get('new_folder_name', '').strip())
    
    if not new_folder_name:
        flash('Please enter a folder name!', 'error')
        return redirect(url_for('files', folder_path=folder_path))
    
    current_path = os.path.join('uploads', folder_path)
    new_folder_path = os.path.join(current_path, new_folder_name)
    
    try:
        os.makedirs(new_folder_path, exist_ok=True)
        flash(f'Folder created successfully!', 'success')
    except Exception as e:
        flash(f'Error creating folder!', 'error')
    
    return redirect(url_for('files', folder_path=folder_path))

@app.route('/preview/<path:file_path>')
def preview_file(file_path):
    full_path = os.path.join('uploads', file_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        # Get file extension to determine content type
        _, ext = os.path.splitext(full_path)
        ext = ext.lower()
        
        # Set appropriate MIME type for text files
        if ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml']:
            return send_file(full_path, as_attachment=False, mimetype='text/plain')
        else:
            return send_file(full_path, as_attachment=False)
    flash('File not found!', 'error')
    return redirect(url_for('files'))

@app.route('/download/<path:file_path>')
def download_file(file_path):
    full_path = os.path.join('uploads', file_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        filename = os.path.basename(file_path)
        return send_file(full_path, as_attachment=True, download_name=filename)
    flash('File not found!', 'error')
    return redirect(url_for('files'))

@app.route('/stream/<path:file_path>')
def stream_file(file_path):
    full_path = os.path.join('uploads', file_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        # Get file extension to determine content type
        _, ext = os.path.splitext(full_path)
        ext = ext.lower()

        # Set appropriate MIME type for video files
        mime_type = None
        if ext == '.mp4':
            mime_type = 'video/mp4'
        elif ext == '.avi':
            mime_type = 'video/x-msvideo'
        elif ext == '.mov':
            mime_type = 'video/quicktime'
        elif ext == '.webm':
            mime_type = 'video/webm'
        elif ext == '.mkv':
            mime_type = 'video/x-matroska'
        elif ext == '.wmv':
            mime_type = 'video/x-ms-wmv'
        elif ext == '.flv':
            mime_type = 'video/x-flv'
        elif ext == '.m4v':
            mime_type = 'video/x-m4v'

        return send_file(full_path, as_attachment=False, mimetype=mime_type)
    flash('File not found!', 'error')
    return redirect(url_for('files'))

@app.route('/delete_item/<path:item_path>')
def delete_item(item_path):
    full_path = os.path.join('uploads', item_path)
    
    # Calculate parent path for redirection
    parent_dir = os.path.dirname(full_path)
    relative_parent = os.path.relpath(parent_dir, 'uploads')
    if relative_parent == '.':
        relative_parent = ''
    
    try:
        if os.path.exists(full_path):
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
                flash(f'Item deleted successfully!', 'delete')
            else:
                os.remove(full_path)
                flash(f'Item deleted successfully!', 'delete')
        else:
            flash('Item not found!', 'error')
    except Exception as e:
        flash(f'Error deleting item!', 'error')
    
    return redirect(url_for('files', folder_path=relative_parent))

@app.route('/rename_item', methods=['POST'])
def rename_item():
    item_path = request.form.get('item_path', '')
    new_name = request.form.get('new_name', '').strip()
    
    if not item_path or not new_name:
        flash('Please provide both item path and new name!', 'error')
        return redirect(url_for('files'))
    
    full_old_path = os.path.join('uploads', item_path)
    
    # Calculate parent path for redirection
    parent_dir = os.path.dirname(full_old_path)
    relative_parent = os.path.relpath(parent_dir, 'uploads')
    if relative_parent == '.':
        relative_parent = ''
    
    if not os.path.exists(full_old_path):
        flash('Item not found!', 'error')
        return redirect(url_for('files', folder_path=relative_parent))
    
    # For files, preserve the extension if not provided in new name
    if os.path.isfile(full_old_path):
        old_name = os.path.basename(full_old_path)
        if '.' in old_name and '.' not in new_name:
            # Get the extension from the old name
            _, ext = os.path.splitext(old_name)
            new_name = new_name + ext
    
    # Secure the filename
    new_filename = secure_filename(new_name)
    full_new_path = os.path.join(parent_dir, new_filename)
    
    # Determine item type before rename
    item_type = 'folder' if os.path.isdir(full_old_path) else 'file'
    
    try:
        # Check if new name already exists
        if os.path.exists(full_new_path):
            flash('An item with that name already exists !', 'error')
            return redirect(url_for('files', folder_path=relative_parent))
        
        # Rename the item
        shutil.move(full_old_path, full_new_path)
        
        flash(f'Item renamed successfully!', 'success')
        
    except OSError as e:
        if item_type == 'folder':
            flash('Cannot rename folder. Close any open files/folders and try again.', 'error')
        else:
            flash(f'Error renaming item!', 'error')
    except Exception as e:
        flash(f'Error renaming item: {str(e)}', 'error')
    
    return redirect(url_for('files', folder_path=relative_parent))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=False)