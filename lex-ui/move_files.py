from os import listdir 
from shutil import copyfile
files_dist_js = listdir('./dist/static/js')
files_dist_css = listdir('./dist/static/css')

out_dir_css = '../mobile-alex-bot/src/assets/app/css/'
out_dir_js = '../mobile-alex-bot/src/assets/app/js/'

def move_file(files, name, ext, input_dir, out_dir):
    correct_file = [file for file in files if name in file and ext in file and '.map' not in file]
    out_file = out_dir + name + '.' + ext
    src = input_dir + correct_file[0]
    copyfile(src, out_file)

def fix_css(file):
    with open(file,'r') as f:
        content = f.read()
        f.close()

    with open(file,'w') as f:
        content = content.replace('/static/','/assets/app/')
        f.write(content)
        f.close()
        
move_file(files_dist_js, 'app', 'js', './dist/static/js/', out_dir_js)
move_file(files_dist_js, 'manifest', 'js', './dist/static/js/', out_dir_js)
move_file(files_dist_js, 'wav-worker', 'js', './dist/static/js/', out_dir_js)
move_file(files_dist_js, 'vendor', 'js', './dist/static/js/', out_dir_js)

move_file(files_dist_css, 'app', 'css', './dist/static/css/', out_dir_css)

fix_css(out_dir_css + 'app.css')